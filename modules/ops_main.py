# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from subprocess import check_call, CalledProcessError

# Ghostsurf Modules
from modules.conf_logging import info, error
from modules.conf_notification import display_notification
from modules.conf_ghostsurf import (
    load_ghostsurf_config,
    save_ghostsurf_config,
)

##############################

# START PROXY

##############################

def start_proxy(
    init_script_file_path,
    start_transparent_proxy_script_file_path,
    is_positive,
    button_label_widget=None,
    ghostsurf_settings_file_path=None,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        if is_positive:
            check_call(["pkexec", "bash", init_script_file_path])
        check_call(["pkexec", "bash", start_transparent_proxy_script_file_path])

        config = load_ghostsurf_config(ghostsurf_settings_file_path)
        config["is_ghostsurf_on"] = "True"
        save_ghostsurf_config(ghostsurf_settings_file_path, config)

        if button_label_widget:
            button_label_widget.setText("Stop")

        message = "Transparent proxy has been turned on."
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except CalledProcessError as e:
        message = "Starting transparent proxy subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while starting transparent proxy."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# STOP PROXY

##############################

def stop_proxy(
    init_script_file_path,
    stop_transparent_proxy_script_file_path,
    is_positive,
    button_label_widget=None,
    ghostsurf_settings_file_path=None,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        if is_positive:
            check_call(["pkexec", "bash", init_script_file_path])
        check_call(["pkexec", "bash", stop_transparent_proxy_script_file_path])

        config = load_ghostsurf_config(ghostsurf_settings_file_path)
        config["is_ghostsurf_on"] = "False"
        save_ghostsurf_config(ghostsurf_settings_file_path, config)

        if button_label_widget:
            button_label_widget.setText("Start")

        message = "Transparent proxy has been turned off."
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except CalledProcessError as e:
        message = "Stopping transparent proxy subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while stopping transparent proxy."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# RESET CHANGES

##############################

def reset_changes(
    reset_script_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        check_call(["pkexec", "bash", reset_script_file_path])
        message = "All changes have been reverted."
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
        info("Changes have been resetted.")
    except CalledProcessError as e:
        message = "Reset subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while resetting."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# UPDATE START/STOP BUTTON TEXT

##############################

def update_start_stop_button_text(
    button_widget,
    ghostsurf_settings_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        config = load_ghostsurf_config(ghostsurf_settings_file_path)
        is_ghostsurf_on = True if config["is_ghostsurf_on"] == "True" else False
        if is_ghostsurf_on:
            button_widget.setText("Stop")
        else:
            button_widget.setText("Start")
    except Exception as e:
        message = "Unexpected error occurred while updating start/stop button's text."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )