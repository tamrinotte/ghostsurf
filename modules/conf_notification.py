# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import subprocess

# Ghostsurf Modules
from modules.conf_logging import error

##############################

# DISPLAY NOTIFICATION

##############################

def display_notification(is_using_gui=False, icon_file_path="", message="", timeout="150"):
    if is_using_gui:
        try:
            notification = subprocess.check_call(
                ["notify-send", "-i", icon_file_path, "-t", timeout, message],
            )
        except subprocess.CalledProcessError as e:
            message = "Notification sending subprocess failed."
            error(f"{message} - {e}")
            return
        except Exception as e:
            message = "Unexpected error occurred while sending notification."
            error(f"{message} - {e}")
            return
    else:
        print(message)