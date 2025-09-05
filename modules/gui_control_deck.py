# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import threading

# Ghostsurf Modules
from modules.conf_logging import (
    debug,
    info,
    error,
)
from modules.conf_notification import display_notification
from modules.conf_dialog import show_question_dialog
from modules.conf_ghostsurf import load_ghostsurf_config
from modules.ops_network import (
    get_public_ip_address,
    change_public_ip_address,
    change_mac_address,
    change_nameservers,
    update_tor_status_label,
)
from modules.ops_system import (
    wipe_memory,
    shred_log_files,
    change_hostname,
    anonymize_browser,
)
from modules.ops_main import (
    reset_changes,
    start_proxy,
    stop_proxy,
    update_start_stop_button_text,
)

##############################

# GLOBAL VARIABLES

##############################

is_using_gui = True

##############################

# START/STOP TRANSPARENT PROXY

##############################

def gui_cd_start_stop_transparent_proxy(
    init_script_file_path,
    start_transparent_proxy_script_file_path,
    stop_transparent_proxy_script_file_path,
    button_label_widget,
    status_label_widget,
    ghostsurf_settings_file_path,
    ghostsurf_logo_file_path
):
    config = load_ghostsurf_config(ghostsurf_settings_file_path)
    is_ghostsurf_on = config["is_ghostsurf_on"] == "True"

    def start_stop_button_question_dialog_processor(i):
        user_answer = i.text()

        if user_answer == "&Yes":
            is_positive = True
        elif user_answer == "&No":
            is_positive = False
        else:
            error("Operation cancelled.")
            return

        def proxy_runner():
            if is_ghostsurf_on:
                stop_proxy(
                    init_script_file_path=init_script_file_path,
                    stop_transparent_proxy_script_file_path=stop_transparent_proxy_script_file_path,
                    is_positive=is_positive,
                    button_label_widget=button_label_widget,
                    ghostsurf_settings_file_path=ghostsurf_settings_file_path,
                    is_using_gui=is_using_gui,
                    ghostsurf_logo_file_path=ghostsurf_logo_file_path,
                )
            else:
                start_proxy(
                    init_script_file_path=init_script_file_path,
                    start_transparent_proxy_script_file_path=start_transparent_proxy_script_file_path,
                    is_positive=is_positive,
                    button_label_widget=button_label_widget,
                    ghostsurf_settings_file_path=ghostsurf_settings_file_path,
                    is_using_gui=is_using_gui,
                    ghostsurf_logo_file_path=ghostsurf_logo_file_path,
                )
            update_tor_status_label(
                label_widget=status_label_widget,
                is_using_gui=is_using_gui,
                ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            )

        proxy_thread = threading.Thread(
            target=proxy_runner,
            daemon=True,
        )
        proxy_thread.start()

    show_question_dialog(
        title="Important",
        text="Do you want to kill dangerous applications and clear dangerous caches?",
        on_click_handler=start_stop_button_question_dialog_processor,
    )

##############################

# UPDATE TOR STATUS LABEL

##############################

def gui_cd_update_tor_status_label(label_widget, ghostsurf_logo_file_path):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to update tor status label...",
        )
        tor_status_thread = threading.Thread(
            target=update_tor_status_label,
            args=[
                label_widget,
                is_using_gui,
                ghostsurf_logo_file_path,
            ],
            daemon=True,
        )
        tor_status_thread.start()
    except Exception as e:
        message = "Failed to start update tor status thread."
        error(f"{message} - {e}")


##############################

# CHANGING IP ADDRESS

##############################

def gui_cd_change_ip(ghostsurf_logo_file_path):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to restart tor service...",
        )
        ip_thread = threading.Thread(
            target=change_public_ip_address,
            args=(is_using_gui, ghostsurf_logo_file_path),
            daemon=True,
        )
        ip_thread.start()
        info("IP change thread started successfully.")
    except Exception as e:
        message = "Failed to start change ip thread."
        error(f"{message} - {e}")

##############################

# SHOW PUBLIC IP ADDRESS

##############################

def gui_cd_show_ip(ghostsurf_logo_file_path):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to connect to the server..."
        )
        ip_thread = threading.Thread(
            target=get_public_ip_address,
            args=(is_using_gui, ghostsurf_logo_file_path,),
            daemon=True
        )
        ip_thread.start()
        info("IP retrieval thread started successfully.")
    except Exception as e:
        message = "Failed to start show ip thread."
        error(f"{message} - {e}")

##############################

# SHRED LOG FILES

##############################

def gui_cd_shred_logs(ghostsurf_logo_file_path, log_shredder_file_path, current_username):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to shred log files..."
        )
        shred_thread = threading.Thread(
            target=shred_log_files,
            args=(
                log_shredder_file_path,
                current_username,
                is_using_gui,
                ghostsurf_logo_file_path,
            ),
            daemon=True
        )
        shred_thread.start()
        info("Shred thread started successfully.")
    except Exception as e:
        message = "Failed to start log shreder thread."
        error(f"{message} - {e}")

##############################

# CHANGE MAC ADDRESS

##############################

def gui_cd_change_mac_address(ghostsurf_logo_file_path, mac_changer_script_file_path):
    def mac_changer_button_question_dialog_processor(i):
        try:
            user_answer = i.text()
            debug(f"Answer to question dialog: {user_answer}")
            if user_answer == "&Yes" or user_answer == "&No":
                display_notification(
                    is_using_gui=is_using_gui,
                    icon_file_path=ghostsurf_logo_file_path,
                    message="Trying to change MAC address..."
                )
            if user_answer == "&Yes":
                is_positive = True
                thread = threading.Thread(
                    target=change_mac_address,
                    args=(mac_changer_script_file_path, is_positive, is_using_gui, ghostsurf_logo_file_path),
                    daemon=True,
                )
            elif user_answer == "&No":
                is_positive = False
                thread = threading.Thread(
                    target=change_mac_address,
                    args=(mac_changer_script_file_path, is_positive, is_using_gui, ghostsurf_logo_file_path),
                    daemon=True,
                )
            else:
                debug("MAC address change operation canceled by user.")

            thread.start()
            info("MAC changer thread started successfully.")
        except Exception as e:
            message = "Failed to start MAC changer thread"
            error(f"{message} - {e}")
    show_question_dialog(
        title="Important",
        text="Do you want to connect back to the internet after changing the MAC address?",
        on_click_handler=mac_changer_button_question_dialog_processor
    )

##############################

# WIPE MEMORY

##############################

def gui_cd_wipe_memory(ghostsurf_logo_file_path, fast_bomb_script_file_path, secure_bomb_script_file_path):
    def wipe_button_question_dialog_processor(i):
        user_answer = i.text()
        if user_answer == "&Yes" or user_answer == "&No":
            message = "Trying to wipe the memory..."
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
        try:
            if user_answer == "&Yes":
                is_positive = True
            elif user_answer == "&No":
                is_positive = False
            else:
                debug("Operation canceled")
                return
            wipe_memory_thread = threading.Thread(
                target=wipe_memory,
                args=[
                    is_positive,
                    fast_bomb_script_file_path,
                    secure_bomb_script_file_path,
                    is_using_gui,
                    ghostsurf_logo_file_path,
                ],
                daemon=True,
            )
            wipe_memory_thread.start()
        except Exception as e:
            message = "Failed to start memory wiper thread."
            error(f"{message} - {e}")
    show_question_dialog(
        title="Important",
        text="Do you want fast and less secure operation?",
        on_click_handler=wipe_button_question_dialog_processor
    )

##############################

# CHANGE DNS NAMESERVERS

##############################

def gui_cd_change_nameservers(
    ghostsurf_logo_file_path,
    working_status,
    nameserver_changer_file_path,
    tor_nameservers_file_path,
    original_resolv_configuration_file_path,
    privacy_focused_nameservers_file_path
):
    try:
        if working_status == "Stop":
            is_working=True
        else:
            is_working=False
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to change nameservers...",
        )
        thread = threading.Thread(
            target=change_nameservers,
            args=[
                is_working,
                nameserver_changer_file_path,
                tor_nameservers_file_path,
                original_resolv_configuration_file_path,
                privacy_focused_nameservers_file_path,
                is_using_gui,
                ghostsurf_logo_file_path,
            ],
            daemon=True
        )
        thread.start()
    except Exception as e:
        message = "Failed to start nameserver changer thread."
        error(f"{message} - {e}")

##############################

# CHANGE HOSTNAME

##############################

def gui_cd_change_hostname(hostname_changer_script_file_path, ghostsurf_logo_file_path):
    def change_hostname_button_question_dialog_processor(i):
        user_answer = i.text()
        if user_answer == "&Yes":
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message="Trying to change system's hostname...",
            )
            hostname_thread = threading.Thread(
                target=change_hostname,
                args=[
                    hostname_changer_script_file_path,
                    is_using_gui,
                    ghostsurf_logo_file_path,
                ],
                daemon=True,
            )
            hostname_thread.start()
        else:
            debug("Operation canceled.")
    show_question_dialog(
        title="Important",
        text="This operation requires reboot. Do you allow to reboot this system?",
        on_click_handler=change_hostname_button_question_dialog_processor,
    )

##############################

# ANONYMIZE BROWSER

##############################

def gui_cd_anonymize_browser(
    init_script_file_path,
    ghostsurf_logo_file_path,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path,
    firefox_profiles_conf_file_path,
):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to create and anonymize Firefox profiles...",
        )
        browser_thread = threading.Thread(
            target=anonymize_browser,
            args=[
                init_script_file_path,
                firefox_profiles_dir,
                custom_firefox_preferences_file_path,
                firefox_profiles_conf_file_path,
                is_using_gui,
                ghostsurf_logo_file_path,
            ],
            daemon=True,
        )
        browser_thread.start()
    except Exception as e:
        message = "Failed to start browser anonymizer thread."
        error(f"{message} - {e}")

##############################

# RESET

##############################

def gui_cd_reset(ghostsurf_logo_file_path, reset_script_file_path):
    def reset_button_question_dialog_processor(i):
        user_answer = i.text()
        if user_answer == "&Yes":
            try:
                display_notification(
                    is_using_gui=is_using_gui,
                    icon_file_path=ghostsurf_logo_file_path,
                    message="Trying to reset...",
                )
                reset_thread = threading.Thread(
                    target=reset_changes,
                    args=(
                        reset_script_file_path,
                        is_using_gui,
                        ghostsurf_logo_file_path,
                    ),
                    daemon=True,
                )
                reset_thread.start()
            except Exception as e:
                message = "Failed to start reset thread."
                error(f"{message} - {e}")
        else:
            debug("Operation canceled.")
            return
    show_question_dialog(
        title="Important",
        text="Are you sure you want to revert all changes and restore the defaults?",
        on_click_handler=reset_button_question_dialog_processor,
    )

##############################

# UPDATE START/STOP BUTTON TEXT

##############################

def gui_update_start_stop_button_text(button_widget, ghostsurf_settings_file_path, ghostsurf_logo_file_path):
    try:
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message="Trying to update start/stop button's text...",
        )
        update_button_text_thread = threading.Thread(
            target=update_start_stop_button_text,
            args=[
                button_widget,
                ghostsurf_settings_file_path,
                is_using_gui,
                ghostsurf_logo_file_path,
            ],
            daemon=True,
        )
        update_button_text_thread.start()
    except Exception as e:
        message = "Failed to start start stop button text updater thread."
        error(f"{message} - {e}")