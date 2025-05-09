#!/bin/bash

main () {
    enable_ipv6
    iptables_accept_all
}

enable_ipv6() {
    sysctl -w net.ipv6.conf.all.disable_ipv6=0 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 >/dev/null 2>&1
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

main