#!/bin/bash

main () {
    # The function which runs the entire script

    # Calling the save_iptables_rules function.
    save_iptables_rules
    
}

save_iptables_rules() {
    # A function which saves iptables rules

    # Saving the iptables rules
    iptables-save > /etc/iptables/rules.v4

}

# Calling the main function
main