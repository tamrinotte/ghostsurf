#!/bin/bash

main () {
    # The main function which runs the entire script

    local nameservers_file_path="$1"
    
    declare_variables "$nameservers_file_path"
    change_nameservers
}

declare_variables() {
    # A function which declares variables

    local nameservers_file_path="$1"
    active_connection_name=$(iwgetid --raw)

    if [ -z "$active_connection_name" ]; then

        active_connection_name=$(nmcli --fields NAME connection show --active | awk 'NR==2 {print $1}')

    fi

    nameservers_string=$(sed -E 's/nameserver\s*//' "$nameservers_file_path" | tr '\n' ',' | sed 's/,$//')

}

change_nameservers() {
    # A function which changes nameservers

    nmcli connection modify "$active_connection_name" ipv4.dns "$nameservers_string"
    nmcli connection down "$active_connection_name"
    nmcli connection up "$active_connection_name"
}

main "$1"