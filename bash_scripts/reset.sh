#!/bin/bash

main() {
    declare_variables
    reset_configuration_files
    enable_ipv6
    reset_mac_address
    restore_firefox_profile
    iptables_accept_all
    reload_system_daemons
}

declare_variables() {
    base_dir=/opt/ghostsurf/_internal
    backup_dir="$base_dir/backup_files"
    username=${SUDO_USER:-${USER}}
    firefox_dir="/home/$username/.mozilla/firefox"
    cache_dir="/home/$username/.cache/mozilla/firefox"
    hosts_file="/etc/hosts"
    network_manager="NetworkManager.service"
    original_hostname=$(cat "$backup_dir/hostname.backup")
    current_hostname=$(hostname)
}

reset_configuration_files() {
    cp "$backup_dir/torrc.backup" /etc/tor/torrc
    cp "$backup_dir/resolv.conf.backup" /etc/resolv.conf
    timedatectl set-timezone "$(cat "$backup_dir/timezone.backup")"
    cp "$backup_dir/hostname.backup" /etc/hostname
    sed -i "s/$current_hostname/$original_hostname/g" "$hosts_file"
}

enable_ipv6() {
    sysctl -w net.ipv6.conf.all.disable_ipv6=0 > /dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 > /dev/null 2>&1
}

reset_mac_address() {
    interfaces=$(ip -o link show | awk -F': ' '{print $2}')
    for iface in $interfaces; do
        [[ "$iface" == "lo" ]] && continue
        ifconfig "$iface" down
        systemctl stop "$network_manager"
        macchanger -p "$iface"
        systemctl start "$network_manager"
        ifconfig "$iface" up
    done
}

restore_firefox_profile() {
    cp "$backup_dir/firefox_profiles.backup" "$firefox_dir/profiles.ini"
    rm -rf "$firefox_dir"/*.ghostsurf
    rm -rf "$cache_dir"/*ghostsurf
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

reload_system_daemons() {
    systemctl --system daemon-reexec
    systemctl daemon-reload
}

main