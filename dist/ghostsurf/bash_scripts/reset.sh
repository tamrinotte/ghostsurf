#!/bin/bash

main () {
    # The main function which runs the entire script

    # Calling the reset_configuration_files function.
    reset_configuration_files

    # Calling the enable_ipv6 function.
    enable_ipv6

    # Calling the reset_mac_address function.
    reset_mac_address

    # Calling the iptables_accept_all function.
    iptables_accept_all

    # Calling the reload_configuration_files function.
    reload_configuration_files

}

declare_variables() {
    # A function which declares variables

    # Getting the original hostname from the backup file
    original_hostname="$(cat /opt/ghostsurf/backup_files/hostname.backup)"

    # Getting the current hostname using a system command
    current_hostname="$(hostname)"

}

reset_configuration_files() {
    # A function which backs up the configuration files that will be replaced by this application

    # Restoring the original torrc file
    cp /opt/ghostsurf/backup_files/torrc.backup /etc/tor/torrc 

    # Restoring the original resolv.conf file
    cp /opt/ghostsurf/backup_files/resolv.conf.backup /etc/resolv.conf 

    # Restoring the original timezone
    timedatectl set-timezone $(cat /opt/ghostsurf/backup_files/timezone.backup)

    # Restoring the original hostname
    cp "/opt/ghostsurf/backup_files/hostname.backup" "/etc/hostname"

    # Replacing the current_hostname in the /etc/hosts file with the original hostname
    sed -i "s/$current_hostname/$original_hostname/g" /etc/hosts

    # Restoring the original prefs.js file
    cp "/opt/ghostsurf/backup_files/prefs.js.backup" "$pref_path" 

}

enable_ipv6() {
    # A function which enables ipv6 connections

    sysctl -w net.ipv6.conf.all.disable_ipv6=0 >/dev/null 2>&1
    sysctl -w net.ipv6.conf.default.disable_ipv6=0 >/dev/null 2>&1

}

reset_mac_address() {

    # Creating a list of network interfaces
    list_of_network_interfaces=$(ip -o link show | awk -F': ' '{print $2}')

    # Iterating over each interface in the list_of_network_interfaces
	for interface in $list_of_network_interfaces; do

        # Checking if the interface is not the loop back interface
        if [[ $interface != "lo" ]]; then

            # Turning the interface down
            ifconfig $interface down

            # Stopping the NetworkManager service
            systemctl stop NetworkManager.service

            # Changing the mac address with random and permanent options
            macchanger -p $interface

            # Starting the NetworkManager service
            systemctl start NetworkManager.service

            # Turning the interface up
            ifconfig $interface up

        fi

    done

}

iptables_accept_all() {
    # A function which deletes all existing iptables rules and accepting everything

    iptables -t filter -F
    iptables -t filter -X
    iptables -t nat -F
    iptables -t nat -X

    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT

}

reload_configuration_files() {
    # A function which reloads configuration files

    systemctl --system daemon-reload

}

# Calling the main function.
main