#!/bin/bash

main () {
    # The main function which runs the entire script
    
    # Calling the declare_variables function.
    declare_variables

    # Calling the change_mac_address function.
    change_mac_address

}

declare_variables() {
    # A function which declares variables

    # Creating a list of network interfaces
    list_of_network_interfaces=$(ip -o link show | awk -F': ' '{print $2}')

}


change_mac_address() {
    # A function which changes the mac address connects back to internet

    # Iterating over each interface in the list_of_network_interfaces
	for interface in $list_of_network_interfaces; do

        # Checking if the interface is not the loop back interface
        if [[ $interface != "lo" ]]; then

            # Turning the interface down
            ifconfig $interface down

            # Stopping the NetworkManager service
            systemctl stop NetworkManager.service

            # Changing the mac address with random and permanent options
            macchanger -rp $interface

            # Starting the NetworkManager service
            systemctl start NetworkManager.service

            # Turning the interface up
            ifconfig $interface up

        fi

    done
    
}

# Calling the main function.
main