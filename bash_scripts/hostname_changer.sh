#!/bin/bash

main () {
    set_random_hostname
}

set_random_hostname(){
    readarray -t array < "/opt/ghostsurf/configuration_files/list_of_fake_hostnames.list"
    current_hostname="$(hostname)"
    array_size=${#array[@]}
    index=$(($RANDOM % $array_size))
    new_hostname="${array[$index]}"
    sed -i "s/$current_hostname/$new_hostname/g" "/etc/hosts"
    if [[ "$new_hostname" != "$current_hostname" ]]
    then
        hostnamectl set-hostname $new_hostname
        systemctl restart NetworkManager.service
    fi
}

main