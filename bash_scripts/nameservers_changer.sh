#!/bin/bash

main () {
    # The main function which runs the entire script

    # Creating a function parameter called username
    local nameservers_file_path="$1"
    
    # Calling declare_variables function
    declare_variables "$nameservers_file_path"

    # Calling change_nameservers funciton
    change_nameservers

}

declare_variables() {
    # A function which declares variables

    # Creating a function parameter called nameservers_file_path
    local nameservers_file_path="$1"

    # Try to get the SSID for Wi-Fi connections
    active_connection_name=$(iwgetid --raw)

    # If there's no SSID (not connected to Wi-Fi), check for Ethernet connections
    if [ -z "$active_connection_name" ]; then

        # Get the name of the active Ethernet connection
        active_connection_name=$(nmcli --fields NAME connection show --active | awk 'NR==2 {print $1}')

    fi

    # Creating a string for nameservers
    nameservers_string=$(sed -E 's/nameserver\s*//' "$nameservers_file_path" | tr '\n' ',' | sed 's/,$//')

}

change_nameservers() {
    # A function which changes nameservers

    nmcli connection modify "$active_connection_name" ipv4.dns "$nameservers_string"
    nmcli connection down "$active_connection_name"
    nmcli connection up "$active_connection_name"

}

# Calling the main function with nameservers_file_path
main "$1"