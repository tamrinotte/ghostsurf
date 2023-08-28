#!/bin/bash

main() {
    # The function which runs the entire script

    # Calling the declare_variables function
    declare_variables

    # Calling the backup_configuration_files function
    backup_configuration_files

    # Calling the set_up_file_ownerships function
    set_up_file_ownerships

}

declare_variables() {
    # A function which declares variables

    # Creating a variable called username which is equal to the logged in user's username
    username=${SUDO_USER:-${USER}}

    # Creating path which lead to the preferences script of firefox
    pref_path=$(find /home/$username -name prefs.js)

}

backup_configuration_files() {
    # A function which backs up the configuration files that will be replaced by this application

    # Backing up the tor configuration file
    sudo cp "/etc/tor/torrc" "/opt/ghostsurf/backup_files/torrc.backup"

    # Backing up the original resolv.conf file
    sudo cp "/etc/resolv.conf" "/opt/ghostsurf/backup_files/resolv.conf.backup"

    # Backing up the original timezone
    sudo timedatectl show | sudo grep Timezone | sudo sed 's/Timezone=//g' > /opt/ghostsurf/backup_files/timezone.backup

    # Backing up the hostname and changing it to a random one
    sudo cp "/etc/hostname" "/opt/ghostsurf/backup_files/hostname.backup"

    # Getting a back up of the original prefs.js file
    sudo cp "$pref_path" "/opt/ghostsurf/backup_files/prefs.js.backup" 
}

set_up_file_ownerships() {
    # A function which sets the file ownerships and permissions

    # Changing the file ownerships recursively
    chown -R $username:$username "/opt/ghostsurf/"

    # Changing the launchers file ownership 
    chown $username:$username "/usr/bin/ghostsurf"

}

# Calling the main function
main
