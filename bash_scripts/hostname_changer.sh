#!/bin/bash

main () {
    set_random_hostname
}

declare_variables() {
    base_dir="/opt/ghostsurf/_internal"
    configuration_dir="$base_dir/configuration_files"
    list_of_fake_hostnames_file_path="$configuration_dir/list_of_fake_hostnames.list"
}

set_random_hostname(){
    readarray -t array < $list_of_fake_hostnames_file_path
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