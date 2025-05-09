#!/bin/bash

main () {
    reset_configuration_files
    enable_ipv6
    reset_mac_address
    delete_ghostsurf_firefox_profile
    iptables_accept_all
    reload_configuration_files
}

declare_variables() {
    original_hostname="$(cat /opt/ghostsurf/backup_files/hostname.backup)"
    current_hostname="$(hostname)"
}

reset_configuration_files() {
    cp /opt/ghostsurf/backup_files/torrc.backup /etc/tor/torrc 
    cp /opt/ghostsurf/backup_files/resolv.conf.backup /etc/resolv.conf 
    timedatectl set-timezone $(cat /opt/ghostsurf/backup_files/timezone.backup)
    cp "/opt/ghostsurf/backup_files/hostname.backup" "/etc/hostname"
    sed -i "s/$current_hostname/$original_hostname/g" /etc/hosts
}

enable_ipv6() {
    sysctl -w net.ipv6.conf.all.disable_ipv6=0 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 >/dev/null 2>&1
}

reset_mac_address() {
    # Creating a list of network interfaces
    list_of_network_interfaces=$(ip -o link show | awk -F': ' '{print $2}')

    # Iterating over each interface in the list_of_network_interfaces
	for interface in $list_of_network_interfaces; do

        if [[ $interface != "lo" ]]; then

            ifconfig $interface down
            systemctl stop NetworkManager.service
            macchanger -p $interface
            systemctl start NetworkManager.service
            ifconfig $interface up

        fi

    done
}

delete_ghostsurf_firefox_profile() {
    cp "/opt/ghostsurf/backup_files/firefox_profiles.backup" "/home/$username/.mozilla/firefox/profiles.ini"

    rm -rf /home/$username/.mozilla/firefox/*.ghostsurf
    rm -rf /home/$username/.cache/mozilla/firefox/*ghostsurf
}

iptables_accept_all() {
    # Flush and delete all user-defined chains in the mangle and raw tables
    iptables -t mangle -F
    iptables -t mangle -X
    iptables -t raw -F
    iptables -t raw -X

    ip6tables -t mangle -F
    ip6tables -t mangle -X
    ip6tables -t raw -F
    ip6tables -t raw -X

    # Flush and delete all user-defined chains in the filter and nat tables
    iptables -t filter -F
    iptables -t filter -X
    iptables -t nat -F
    iptables -t nat -X
    
    ip6tables -t filter -F
    ip6tables -t filter -X
    ip6tables -t nat -F
    ip6tables -t nat -X

    # Zero counters
    iptables -Z
    ip6tables -Z

    # Reset default policies
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT

    ip6tables -P INPUT ACCEPT
    ip6tables -P FORWARD ACCEPT
    ip6tables -P OUTPUT ACCEPT
}

reload_configuration_files() {
    systemctl --system daemon-reload
}

main