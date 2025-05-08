# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from time import sleep
from subprocess import run, check_call, CalledProcessError
from re import compile
from threading import Thread
from pathlib import Path

# PySide6
from PySide6.QtWidgets import QMessageBox

# Ghostsurf Modules
from modules.logging_config import (
    debug,
    info,
    warning,
    error,
)
from modules.notification_config import display_notification



##############################

# SUB FUNCTIONS

##############################

def less_secure_memory_wipe(
    ghostsurf_logo_file_path,
    fast_bomb_script_file_path
):

    try:

        check_call(["pkexec", fast_bomb_script_file_path])

    except CalledProcessError as e:

        error(f"Error: {e}")
        return

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Caches are dropped and memory is wiped.")

def high_secure_memory_wipe(ghostsurf_logo_file_path, secure_bomb_script_file_path):

    try:

        check_call(["pkexec", secure_bomb_script_file_path])

    except CalledProcessError as e:

        error(f"Error: {e}")
        return

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Caches are dropped and memory is wiped.")

def change_the_mac_address_and_connect_back_to_wifi(ghostsurf_logo_file_path, mac_changer_script_file_path):

    internet_adaptor_name = run(
        ["ip route show default | awk '/default/ {print $5}'"],
        shell=True,
        capture_output=True, text=True
    ).stdout.strip()
    command_string = f"{mac_changer_script_file_path} && sleep 4 && nmcli d connect {internet_adaptor_name}"

    try:

        check_call(["pkexec", "bash", "-c", command_string])

    except CalledProcessError as e:

        error(f"Error: {e}")
        return

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Mac address has been changed.")

def change_ns(
    ghostsurf_logo_file_path,
    working_status,
    nameserver_changer_file_path,
    tor_nameservers_file_path,
    original_resolv_configuration_file_path,
    privacy_focused_nameservers_file_path
):

    if working_status == "Stop":

        command_string = (
            f"{nameserver_changer_file_path} {tor_nameservers_file_path} && "
            f"cp {tor_nameservers_file_path} {original_resolv_configuration_file_path}"
        )

    else:

        command_string = (
            f"{nameserver_changer_file_path} {privacy_focused_nameservers_file_path} && "
            f"cp {privacy_focused_nameservers_file_path} {original_resolv_configuration_file_path}"
        )

    try:

        check_call(["pkexec", "bash", "-c", command_string])

    except CalledProcessError as e:

        error(f"Error: {e}")
        return

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Nameservers has been changed.")


##############################

# MAIN FUNCTIONS

##############################

def gui_cd_show_ip(ghostsurf_logo_file_path):

    sleep(1.5)
    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Trying to connect to the server.")
    sleep(1.5)

    try:

        public_ip_address = run(
            ["curl", "--connect-timeout", "7.5", "https://ifconfig.io"],
            capture_output=True,
            text=True
        ).stdout.strip()
        ip_addr_regex = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')
        result = ip_addr_regex.search(public_ip_address).group()

        if result == public_ip_address:

            message = f'Your public ip address is {public_ip_address}.'

        else:
 
            message = "Couldn't connect to the server!"

    except:

        message = "Couldn't connect to the server!"

    display_notification(icon_file_path=ghostsurf_logo_file_path, message=message)

def gui_cd_shred_logs(ghostsurf_logo_file_path, log_shredder_file_path, current_username):

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Shreading the log files.")
    sleep(0.3)

    try:

        check_call(["pkexec", log_shredder_file_path])

    except CalledProcessError as e:

        error(f"Error: {e}")
        return

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Log shredding has been done.")

def gui_cd_reset(ghostsurf_logo_file_path, reset_iptables_only_script_file_path, reset_script_file_path):

    def reset_button_question_dialog_processor(i):

        user_answer = i.text()
        sleep(0.3)

        if user_answer == "&Yes":

            display_notification(icon_file_path=ghostsurf_logo_file_path, message="Resetting iptables rules only.")
            sleep(0.3)

            try:

                check_call(["pkexec", reset_iptables_only_script_file_path])

            except CalledProcessError as e:

                error(f"Error: {e}")
                return

            display_notification(icon_file_path=ghostsurf_logo_file_path, message="Iptables rules are reset.")
 
        elif user_answer == "&No":

            display_notification(
                icon_file_path=ghostsurf_logo_file_path,
                message="Resetting ghostsurf configurations."
            )
            sleep(0.3)

            try:

                check_call(["pkexec", reset_script_file_path])

            except CalledProcessError as e:

                error(f"Error: {e}")
                return

            display_notification(icon_file_path=ghostsurf_logo_file_path, message="Reseting is done.")

        else:

            debug("Operation canceled")

    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("Do you want to reset iptables rules only?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.buttonClicked.connect(reset_button_question_dialog_processor)
    question_dialog.exec_()

def gui_cd_change_mac_address(ghostsurf_logo_file_path, mac_changer_script_file_path):

    def mac_changer_button_question_dialog_processor(i):

        user_answer = i.text()

        if user_answer == "&Yes":

            mac_changer_thread = Thread(
                target=change_the_mac_address_and_connect_back_to_wifi,
                args=[ghostsurf_logo_file_path, mac_changer_script_file_path]
            )
            mac_changer_thread.start()

        elif user_answer == "&No":

            try:

                check_call(["pkexec", mac_changer_script_file_path])

            except CalledProcessError as e:

                error(f"Error: {e}")
                return

            display_notification(icon_file_path=ghostsurf_logo_file_path, message="Mac address has been changed.")

        else:

            debug("Operation canceled")

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Changing the mac address.")

    sleep(0.3)
    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("Do you want to connect back to the internet?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.buttonClicked.connect(mac_changer_button_question_dialog_processor)
    question_dialog.exec_()

def gui_cd_wipe_memory(ghostsurf_logo_file_path, fast_bomb_script_file_path, secure_bomb_script_file_path):

    def wipe_button_question_dialog_processor(i):
        
        user_answer = i.text()
        sleep(0.3)

        if user_answer == "&Yes":

            display_notification(
                icon_file_path=ghostsurf_logo_file_path,
                message="Wiping the memory and droping caches. This might take some time!"
            )
            wipe_memory_thread = Thread(
                target=less_secure_memory_wipe,
                args=[ghostsurf_logo_file_path, fast_bomb_script_file_path]
            )
            wipe_memory_thread.start()

        elif user_answer == "&No":

            display_notification(
                icon_file_path=ghostsurf_logo_file_path,
                message="Wiping the memory and droping caches. This might take some time!"
            )
            wipe_memory_thread = Thread(
                target=high_secure_memory_wipe,
                args=[ghostsurf_logo_file_path, secure_bomb_script_file_path]
            )
            wipe_memory_thread.start()

        else:

            debug("Operation canceled")

    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("Do you want fast and less secure operation?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.buttonClicked.connect(wipe_button_question_dialog_processor)
    question_dialog.exec_()

def gui_cd_change_nameservers(
    ghostsurf_logo_file_path,
    working_status,
    nameserver_changer_file_path,
    tor_nameservers_file_path,
    original_resolv_configuration_file_path,
    privacy_focused_nameservers_file_path
):

    display_notification(icon_file_path=ghostsurf_logo_file_path, message="Changing the nameservers.")
    sleep(0.3)
    thread = Thread(
        target=change_ns,
        args=[
            ghostsurf_logo_file_path,
            working_status,
            nameserver_changer_file_path,
            tor_nameservers_file_path,
            original_resolv_configuration_file_path,
            privacy_focused_nameservers_file_path
        ]
    )
    thread.start()

def gui_cd_anonymize_browser(
    init_script_file_path,
    ghostsurf_logo_file_path,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path,
    firefox_profiles_conf_file_path
):

    ghostsurf_profile_pattern = compile(r".*ghostsurf$")
    penetration_testing_pattern = compile(r".*penetration-testing$")
    
    is_ghostsurf_profile_exists = False
    is_penetration_testing_profile_exists = False

    for profile_path in firefox_profiles_dir.iterdir():

        if profile_path.is_dir() and ghostsurf_profile_pattern.match(profile_path.name):
            
            debug(f"Found ghostsurf profile: {profile_path}")
            is_ghostsurf_profile_exists = True
                    
    for profile_path in firefox_profiles_dir.iterdir():

        if profile_path.is_dir() and penetration_testing_pattern.match(profile_path.name):
            
            debug(f"Found penetration-testing profile: {profile_path}")
            is_penetration_testing_profile_exists = True

    if is_ghostsurf_profile_exists == False:

        display_notification(icon_file_path=ghostsurf_logo_file_path, message="Creating Ghostsurf Firefox profile.")
        sleep(2)
        run(["firefox-esr", "-CreateProfile", "ghostsurf"], text=True)
        
        if custom_firefox_preferences_file_path.exists() == True:

            with open(custom_firefox_preferences_file_path, "r") as the_custom_prefs_file:
                custom_prefs = the_custom_prefs_file.read()

        else:

            display_notification(
                icon_file_path=ghostsurf_logo_file_path,
                message="Custom preferences file not found. Try to reinstall ghostsurf!"
            )

        ghostsurf_firefox_profile_dir = next(Path(firefox_profiles_dir).glob("*.ghostsurf"))
        debug(f"Ghostsurf Firefox profile dir path = {ghostsurf_firefox_profile_dir}")

        if ghostsurf_firefox_profile_dir is not None:
            # Construct the path to user.js
            ghostsurf_firefox_profile_file_path = Path(ghostsurf_firefox_profile_dir, "user.js")
            debug(f"Ghostsurf Firefox profile file path = {ghostsurf_firefox_profile_file_path}")

        with open(ghostsurf_firefox_profile_file_path, "w") as ghostsurf_firefox_profile_user_pref_file:
            ghostsurf_firefox_profile_user_pref_file.write(custom_prefs)

        try:

            check_call(["pkexec", init_script_file_path])

        except CalledProcessError as e:

            error(f"Error: {e}")
            return

        with open(firefox_profiles_conf_file_path, "r") as firefox_prof_conf_file:
            firefox_prof_conf_lines = firefox_prof_conf_file.readlines()

        for line in firefox_prof_conf_lines:

            if "Path" in line:

                path = line.split("=")[1][:-1]

                if "ghostsurf" in path:

                    ghostsurf_profile_path_spec = path

                elif "default" in path:

                    default_profile_path_spec = path

            elif "Default" in line and "." in line:

                path = line.split("=")[1][:-1]
                default_profile_setting_raw = line

        new_default = f"Default={ghostsurf_profile_path_spec}\n"
        firefox_prof_conf_lines[firefox_prof_conf_lines.index(default_profile_setting_raw)] = new_default

        with open(firefox_profiles_conf_file_path, "w") as f:
            f.write("".join(firefox_prof_conf_lines))

        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="Ghostsurf Firefox profile has been created. And, preferences has been set."
        )

    else:

        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="Ghostsurf Firefox profile already exists."
        )

    if is_penetration_testing_profile_exists == False:

        sleep(2)
        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="Creating Penetration-Testing Firefox profile."
        )
        sleep(2)
        run(["firefox-esr", "-CreateProfile", "penetration-testing"], text=True)
        sleep(2)
        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="Penetration-Testing Firefox profile has been created."
        )

    else:

        sleep(2)
        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="Penetration-Testing Firefox profile already exists."
        )

def gui_cd_change_hostname(hostname_changer_script_file_path):

    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("This operation requires reboot. Do you allow to reboot this system?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog_answer = question_dialog.exec()

    if question_dialog_answer == QMessageBox.Yes:

        debug("Rebooting the system")
        run(["pkexec", "bash", "-c", f"{hostname_changer_script_file_path} && reboot"])

    else:

        debug("Operation canceled")