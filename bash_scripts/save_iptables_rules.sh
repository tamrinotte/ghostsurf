#!/bin/bash

main () {
    # The function which runs the entire script

    save_iptables_rules
}

save_iptables_rules() {
    # A function which saves iptables rules

    iptables-save > /etc/iptables/rules.v4
}

main