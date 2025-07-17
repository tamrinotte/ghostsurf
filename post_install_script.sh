#!/bin/bash

main() {
    declare_variables
    backup_configuration_files
    set_up_file_ownerships
}

declare_variables() {
    username=${SUDO_USER:-${USER}}
}

backup_configuration_files() {
    sudo cp "/etc/tor/torrc" "/opt/ghostsurf/_internal/backup_files/torrc.backup"
    sudo cp "/etc/resolv.conf" "/opt/ghostsurf/_internal/backup_files/resolv.conf.backup"
    sudo timedatectl show | sudo grep Timezone | sudo sed 's/Timezone=//g' > /opt/ghostsurf/_internal/backup_files/timezone.backup
    sudo cp "/etc/hostname" "/opt/ghostsurf/_internal/backup_files/hostname.backup"
    sudo cp "/home/$username/.mozilla/firefox/profiles.ini" "/opt/ghostsurf/_internal/backup_files/firefox_profiles.backup"
}

set_up_file_ownerships() {
    chown -R $username:$username "/opt/ghostsurf/"
    chown $username:$username "/usr/bin/ghostsurf"
    chown root:root -R "/opt/ghostsurf/_internal/bash_scripts"
}

main