#!/bin/bash

main() {
    declare_variables
    backup_configuration_files
    set_up_file_ownerships
}

declare_variables() {
    username=${SUDO_USER:-${USER}}
    base_dir="/opt/ghostsurf"
    internal_dir="$base_dir/_internal"
    backup_dir="$internal_dir/backup_files"
    torrc_backup_file_path="$backup_dir/torrc.backup"
    resolv_configuration_backup_file_path="$backup_dir/resolv.conf.backup"
    timezone_backup_file_path="$backup_dir/timezone.backup"
    hostname_backup_file_path="$backup_dir/hostname.backup"
    firefox_profiles_backup_file_path="$backup_dir/firefox_profiles.backup"
    bash_scripts_dir="$internal_dir/bash_scripts"
}

backup_configuration_files() {
    sudo cp "/etc/tor/torrc" $torrc_backup_file_path
    sudo cp "/etc/resolv.conf" $resolv_configuration_backup_file_path
    sudo timedatectl show | sudo grep Timezone | sudo sed 's/Timezone=//g' > $timezone_backup_file_path
    sudo cp "/etc/hostname" $hostname_backup_file_path
    sudo cp "/home/$username/.mozilla/firefox/profiles.ini" $firefox_profiles_backup_file_path
}

set_up_file_ownerships() {
    chown -R $username:$username $base_dir
    chown $username:$username "/usr/bin/ghostsurf"
    chown root:root -R $bash_scripts_dir
}

main