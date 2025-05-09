#!/bin/bash

main() {
    declare_variables
    drop_timezone_change
    enable_ipv6
    delete_all_rules
    default_accept
    systemctl stop tor
    restore_default_configuration_files
    systemctl --system daemon-reload
}

declare_variables() {
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
    timedatectl set-timezone $original_timezone
}

enable_ipv6() {
    sysctl -w net.ipv6.conf.all.disable_ipv6=0 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 >/dev/null 2>&1
}

delete_all_rules() {
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
}

default_accept() {
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT

    ip6tables -P INPUT ACCEPT
    ip6tables -P FORWARD ACCEPT
    ip6tables -P OUTPUT ACCEPT
}

restore_default_configuration_files() {
    cp $torrc_backup_file_path $torrc_file_path
    cp $privacy_focused_nameservers_file_path $resolvconf_file_path
}

main