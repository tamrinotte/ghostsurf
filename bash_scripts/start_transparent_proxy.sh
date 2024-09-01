#!/bin/bash

main() {
    # The main function which runs the entire script

    declare_variables
    systemctl start tor
    disable_ipv6
    set_timezone_change
    setup_configuration_files
    set_up_iptables_rules
    systemctl restart tor
}

declare_variables() {
    # A function which declares variables
   
    tor_uid="$(id -u debian-tor)"
    non_tor="127.0.0.0/8 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16"
    trans_port="9040"
    dns_port="5353"
    virtual_address="10.192.0.0/10"
    torrc_file_path="/etc/tor/torrc"
    resolvconf_file_path="/etc/resolv.conf"
    custom_torrc_file="/opt/ghostsurf/configuration_files/torrc.custom"
    custom_resolv_conf_file="/opt/ghostsurf/configuration_files/tor_nameservers_resolv.conf"
}

set_timezone_change() {
    # A function which changes the timezone

    # Setting a new timezone
    timedatectl set-timezone UTC &> /dev/null
}

disable_ipv6() {
    # A function which disables ipv6 connections
    
    # disable IPv6
    sysctl -w net.ipv6.conf.all.disable_ipv6=1 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=1 >/dev/null 2>&1
}

setup_configuration_files() {
    # A function which backs up the resolv.conf file

    cp $custom_resolv_conf_file $resolvconf_file_path
    cp $custom_torrc_file $torrc_file_path

    systemctl --system daemon-reload
}

set_up_iptables_rules() {
    # A function which sets up iptables rules
    
    # Flush All Iptables Chains/Firewall rules
    iptables -F
    
    # Delete all Iptables Chains
    iptables -X
    
    # Flush all counters
    iptables -Z 

    # Flush and delete all nat and mangle
    iptables -t mangle -F
    iptables -t mangle -X
    iptables -t raw -F
    iptables -t raw -X

    iptables -t filter -F
    iptables -t filter -X
    iptables -t nat -F
    iptables -t nat -X

    # Accept all traffic
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    
    ## *nat OUTPUT (For local redirection)
    #
    # nat .onion addresses
    iptables -t nat -A OUTPUT -d $virtual_address -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j REDIRECT --to-ports $trans_port

    # nat dns requests to Tor
    iptables -t nat -A OUTPUT -d 127.0.0.1/32 -p udp -m udp --dport 53 -j REDIRECT --to-ports $dns_port

    # Don't nat the Tor process, the loopback, or the local network
    iptables -t nat -A OUTPUT -m owner --uid-owner $tor_uid -j RETURN
    iptables -t nat -A OUTPUT -o lo -j RETURN

    # Allow lan access for hosts in $non_tor
    for lan in $non_tor; do
        iptables -t nat -A OUTPUT -d $lan -j RETURN
    done

    # Redirects all other pre-routing and output to Tor's TransPort
    iptables -t nat -A OUTPUT -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j REDIRECT --to-ports $trans_port

    ## *filter INPUT
    iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT
    iptables -A INPUT -i lo -j ACCEPT

    # Drop everything else
    iptables -A INPUT -j DROP

    ## *filter FORWARD
    iptables -A FORWARD -j DROP

    ## *filter OUTPUT
    #
    # Fix for potential kernel transproxy packet leaks
    # see: https://lists.torproject.org/pipermail/tor-talk/2014-March/032507.html
    iptables -A OUTPUT -m conntrack --ctstate INVALID -j DROP

    iptables -A OUTPUT -m state --state INVALID -j DROP
    iptables -A OUTPUT -m state --state ESTABLISHED -j ACCEPT

    # Allowing Tor process output
    iptables -A OUTPUT -m owner --uid-owner $tor_uid -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT

    # Allowing loopback output
    iptables -A OUTPUT -d 127.0.0.1/32 -o lo -j ACCEPT

    # Doing the Tor transproxy magic
    iptables -A OUTPUT -d 127.0.0.1/32 -p tcp -m tcp --dport $trans_port --tcp-flags FIN,SYN,RST,ACK SYN -j ACCEPT

    # Dropping everything else
    iptables -A OUTPUT -j DROP

    # Setting the default policies to DROP
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
}

main