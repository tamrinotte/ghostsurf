#!/bin/bash

main () {
    declare_variables
    change_mac_address
}

declare_variables() {
    # Creating a list of network interfaces
    list_of_network_interfaces=$(ip -o link show | awk -F': ' '{print $2}')
}


change_mac_address() {
    # Iterating over each interface in the list_of_network_interfaces
	for interface in $list_of_network_interfaces
    do
        if [[ $interface != "lo" ]]
        then
            ifconfig $interface down
            systemctl stop NetworkManager.service
            macchanger -rp $interface
            ifconfig $interface up
            systemctl start NetworkManager.service
        fi
    done
}

main