#!/bin/bash

main () {
    # The function which runs the entire script

    set_random_hostname
}

set_random_hostname(){
    # A function which sets a random hostname

    ## Benefits of changing hostname:
    ### Reducing Identifiability: The hostname of a device is often used as part of its network identification. By default, devices may have hostnames that include identifiable information, such as the device owner's name or the device model. Changing the hostname to a more generic or random name can help reduce the risk of being easily identified or traced back to a specific individual or device.
    ### Mitigating Network Scanning: In certain scenarios, attackers or malicious actors may conduct network scanning to identify vulnerable devices or targets. By changing the hostname, you make it more challenging for them to discern information about your device and potentially decrease the likelihood of being targeted. Ex: Modems are loogging your hostname.
    ### Enhancing Privacy: The hostname of a device can sometimes be used in various network protocols or log files, potentially revealing information about the device and its owner. Changing the hostname can help protect your privacy by reducing the exposure of personal or identifiable information.

    # Read the list_of_fake_hostnames.list file and populate the array
    readarray -t array < "/opt/ghostsurf/configuration_files/list_of_fake_hostnames.list"

    current_hostname="$(hostname)"

    # Identifying the size of the array
    size=${#array[@]}

    # Creating a random index variable
    index=$(($RANDOM % $size))

    # Selecting random hostname from the list of hostnames
    new_hostname="${array[$index]}"
    
    # Find the current hostname in the /ets/hosts file and replace it with the new name
    sed -i "s/$current_hostname/$new_hostname/g" "/etc/hosts"

    hostnamectl set-hostname $new_hostname

    systemctl restart NetworkManager.service
}

main