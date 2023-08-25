#!/bin/bash

main () {
    # The function which runs the entire script

    # Calling the set_random_hostname function.
    set_random_hostname
}

set_random_hostname(){
    # A function which sets a random hostname

    ## Benefits of changing hostname:
    ### Reducing Identifiability: The hostname of a device is often used as part of its network identification. By default, devices may have hostnames that include identifiable information, such as the device owner's name or the device model. Changing the hostname to a more generic or random name can help reduce the risk of being easily identified or traced back to a specific individual or device.
    ### Mitigating Network Scanning: In certain scenarios, attackers or malicious actors may conduct network scanning to identify vulnerable devices or targets. By changing the hostname, you make it more challenging for them to discern information about your device and potentially decrease the likelihood of being targeted.
    ### Enhancing Privacy: The hostname of a device can sometimes be used in various network protocols or log files, potentially revealing information about the device and its owner. Changing the hostname can help protect your privacy by reducing the exposure of personal or identifiable information.

    # Creating an array of random hostnames
    array[0]="Windows10-Enterprise "
    array[1]="Windows10-Pro"
    array[2]="Windows10-Enterprise-LTSC "
    array[3]="Windows8.1O-EM"
    array[4]="Windows8-Enterprise"
    array[5]="Windows8.1-Pro"
    array[6]="Windows7-Professional"
    array[7]="Windows7-Enterprise"
    array[8]="Windows7-Ultimate"
    array[9]="Windows-Vista-Business"
    array[10]="WindowsXP-Professional"
    array[11]="macOS11"
    array[12]="OSX10.11"
    array[13]="MacBook-Air"
    array[14]="MacBook"
    array[15]="MacBook-Pro"

    # Creating a variable from the current hostname
    current_hostname="$(hostname)"

    # Identifying the size of the array
    size=${#array[@]}

    # Creating a random index variable
    index=$(($RANDOM % $size))

    # Selecting random hostname from the list of hostnames
    new_hostname="${array[$index]}"
    
    # Find the current hostname in the /ets/hosts file and replace it with the new name
    sed -i "s/$current_hostname/$new_hostname/g" "/etc/hosts"

    # Updating the hostname of the system
    hostnamectl set-hostname $new_hostname

    # Restarting the network manager
    systemctl restart NetworkManager.service

}

# Calling the main function
main