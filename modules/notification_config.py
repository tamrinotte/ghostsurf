# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from subprocess import run
from os import system

def display_notification(icon_file_path, message, timeout="150"):

    notification = run(
        ["notify-send", "-i", icon_file_path, "-t", timeout, message],
        text=True
    )

    if notification.returncode != 0:

        system(f"notify-send -i {icon_file_path} -t {timeout} {message}")
