#!/bin/bash

main() {
    # The main function which runs the entire script

    declare_variables
    drop_timezone_change
    enable_ipv6
    delete_all_rules
    default_drop
    allow_input_output_on_loopback_interfaces
    set_iptables_rules
    append_rules_for_essential_security_measures
    save_the_rules
    systemctl stop tor
    restore_default_configuration_files
}

declare_variables() {
    # A function which declares variables

    original_timezone=$(cat /opt/ghostsurf/backup_files/timezone.backup)
    pref_path="$(find /home -name prefs.js)"
    torrc_file_path="/etc/tor/torrc"
    torrc_backup_file_path="/opt/ghostsurf/backup_files/torrc.backup"
    resolvconf_file_path="/etc/resolv.conf"
    privacy_focused_nameservers_file_path="/opt/ghostsurf/configuration_files/privacy_focused_nameservers_resolv.conf"
    rules_v4_file_path="/etc/iptables/rules.v4"
    rules_v6_file_path="/etc/iptables/rules.v6"
}

drop_timezone_change() {
    # A function which changes the timezone

    timedatectl set-timezone $original_timezone
}

enable_ipv6() {
    # A function which enables ipv6 connections

    sysctl -w net.ipv6.conf.all.disable_ipv6=0 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 >/dev/null 2>&1

}

delete_all_rules() {
    # A function which deletes all existing iptables rules for ipv4 and ipv6

    # Clearing the previous rules
    iptables -t filter -F
    iptables -t filter -X
    iptables -t nat -F
    iptables -t nat -X

    ip6tables -t filter -F
    ip6tables -t filter -X
    ip6tables -t nat -F
    ip6tables -t nat -X
}

default_drop() {
    # A function which drop all packages coming into, coming into the server but that are routed to somewhere else and coming out of the server.
    
    # Default Drop: Drop all packages coming into, coming into the server but that are routed to somewhere else and coming out of the server. So, the packages can be accepted, sended or, routed only in the ways that you stated.
    # INPUT Chain: Network packages coming into the server.
    # FORWARD Chain: Network packages coming into the server that are routed to somewhere else.
    # OUTPUT Chain: Network packages coming out to Linux server.
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP

    ip6tables -P INPUT DROP
    ip6tables -P FORWARD DROP
    ip6tables -P OUTPUT DROP
}

allow_input_output_on_loopback_interfaces() {
    # A function which allows input and output on the loopback interface

    # Loopback: The loopback device is a special, virtualnetwork interface that your computer uses to communicate with itself. It is used mainly for diagnostics and troubleshooting, and to connect to servers running on the local machine. · The Purpose of Loopback · When a network interface is disconnected--for example, when an Ethernet port is unplugged or Wi-Fi is turned off or not associated with an access point--no communication on that interface is possible, not even communication between your computer and itself. The loopback interface does not represent any actual hardware, but exists so applications running on your computer can always connect to servers on the same machine. · This is important for troubleshooting (it can be compared to looking in a mirror). The loopback device is sometimes explained as purely a diagnostic tool. But it is also helpful when a server offering a resource you need is running on your own machine.
    # You need the allow the communications with this interface to be able use your computer to communicate with services.
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT

    ip6tables -A INPUT -i lo -j ACCEPT
    ip6tables -A OUTPUT -o lo -j ACCEPT
}

set_iptables_rules() {
    # A function which sets iptables rules for ipv4

    # HTTP: Hypertext Transfer Protocol -> The purpose of the HTTP protocol is to provide a standard way for web browsers and servers to talk to each other.
    # These policies are required if you want to be able to connect to internet using http and https protocols. These are the most common ones and the standard way for web browsers and servers to talk to each other.
    iptables -A INPUT -p tcp -m conntrack --ctstate ESTABLISHED,RELATED --sport 80 -j ACCEPT
    iptables -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT

    # HTTPS: Hypertext Transfer Protocol Secure -> The purpose of the HTTP protocol is to provide a standard way for web browsers and servers to talk to each other with a extensive security that prevents man in the middle and etc.
    iptables -A INPUT -p tcp -m conntrack --ctstate ESTABLISHED,RELATED --sport 443 -j ACCEPT
    iptables -A OUTPUT -p tcp -m tcp --dport 443 -j ACCEPT

    # DNS: Domain Name System -> The purpose of DNS is to translate a domain name into the appropriate IP address.
    # Note: You should allow incoming and out going communications to this port if you want to use URLs instead of ipaddresses. Ex-URL: www.google.com 
    iptables -A INPUT -p udp --sport 53 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT    
    iptables -A OUTPUT -p udp --dport 53 -m udp -j ACCEPT
}

append_rules_for_essential_security_measures() {
    # A function which appends firewall rules for essential security

    # Logging                                                                                                                
    iptables -A INPUT -j LOG --log-prefix "IPTABLES-DROP: " --log-level 4                                                                                                                     
    iptables -A OUTPUT -j LOG --log-prefix "IPTABLES-DROP: " --log-level 4
                                                                                                                                                                     
    # Drop invalid packets                                                                                                                                   
    iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
                                                                                                                                                     
    # Drop packets with too many fragments
    iptables -A INPUT -f -j DROP
                                                                                                                                                               
    # Drop incoming NULL packets                                                                                                                                      
    iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
                                                                                                                                                                        
    # Drop XMAS packets                                                                                                                                       
    iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
                                                                                                                                                                     
    # Drop SYN-FIN packets                                                                                                                               
    iptables -A INPUT -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
                                                                                                                                                                   
    # Drop malformed packets                                                                                                                                   
    iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
                                                                                                                                         
    # Prevent DoS attacks (Adjust threshold as needed)                                                                                                 
    iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
                                                                                                                                                           
    # Drop all other incoming traffic
    iptables -A INPUT -j DROP

    # Reject outgoing traffic for unkown destinations                                                                                                                                          
    iptables -A OUTPUT -d 0.0.0.0/8 -j REJECT
    iptables -A OUTPUT -d 127.0.0.0/8 -j REJECT 
    iptables -A OUTPUT -d 224.0.0.0/4 -j REJECT 
    iptables -A OUTPUT -d 240.0.0.0/5 -j REJECT 
    iptables -A OUTPUT -d 255.255.255.255 -j REJECT

    # Drop packets with suspicious flags
    iptables -A INPUT -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP

    # Drop packets with too many TCP options
    iptables -A INPUT -p tcp --tcp-options 6:10 -j DROP

    # Drop packets with invalid IP addresses
    iptables -A INPUT -s 0.0.0.0/0 -j DROP

    iptables -A INPUT -d 0.0.0.0/0 -j DROP
}

save_the_rules() {
    # A function which saves the rules to make them persistent

    iptables-save > $rules_v4_file_path
    ip6tables-save > $rules_v6_file_path
}

restore_default_configuration_files() {
    # A function which restores the default configuration files. Hint: Ghostsurf defaults baby!!. Reset if you don't like them.

    cp $torrc_backup_file_path $torrc_file_path
    cp $privacy_focused_nameservers_file_path $resolvconf_file_path

    systemctl --system daemon-reload
}

main