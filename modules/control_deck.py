# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from time import sleep
from subprocess import run
from re import compile
from threading import Thread
from pathlib import Path
from logging import basicConfig, DEBUG, debug, disable, CRITICAL

# PySide6
from PySide6.QtWidgets import QMessageBox

# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)



##############################

# SUB FUNCTIONS

##############################

def less_secure_memory_wipe(user_pwd, ghostsurf_logo_file_path, fast_bomb_script_file_path):
    """A function which runs a fast memory wipe"""

    run(["sudo", "-S", fast_bomb_script_file_path], text=True, input=user_pwd)
    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Caches are dropped and memory is wiped."], text=True)

def high_secure_memory_wipe(user_pwd, ghostsurf_logo_file_path, secure_bomb_script_file_path):
    """A function which runs a secure memory wipe"""

    run(["sudo", "-S", secure_bomb_script_file_path], text=True, input=user_pwd)
    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Caches are dropped and memory is wiped."], text=True)

def change_the_mac_address_and_connect_back_to_wifi(user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path):
    """A function which changes the computer's mac address and connects back to the internet"""

    internet_adaptor_name = run(["ip route show default | awk '/default/ {print $5}'"], shell=True, capture_output=True, text=True).stdout.strip()
    run(["sudo", "-S", mac_changer_script_file_path], text=True, input=user_pwd)
    sleep(4)
    run(["sudo", "-S", "nmcli", "d", "connect", internet_adaptor_name], text=True, input=user_pwd)
    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Mac address has been changed."], text=True)

def change_ns(user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path):
    """A function which changes the name servers"""

    if working_status == "Stop":

        run(["sudo", "-S", nameserver_changer_file_path, tor_nameservers_file_path], text=True, input=user_pwd)
        run(["sudo", "-S", "cp", tor_nameservers_file_path, original_resolv_configuration_file_path], text=True, input=user_pwd)

    else:

        run(["sudo", "-S", nameserver_changer_file_path, privacy_focused_nameservers_file_path], text=True, input=user_pwd)
        run(["sudo", "-S", "cp", privacy_focused_nameservers_file_path, original_resolv_configuration_file_path], text=True, input=user_pwd)

    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Nameservers has been changed."], text=True)


##############################

# MAIN FUNCTIONS

##############################

def cd_show_ip(user_pwd, ghostsurf_logo_file_path):
    """A function which tries to displays the user's public ip address with notifications"""

    sleep(1.5)
    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Trying to connect to the server."], text=True)
    sleep(1.5)

    try:

        public_ip_address = run(["curl", "--connect-timeout", "7.5", "https://ifconfig.io"], capture_output=True, text=True).stdout.strip()
        ip_addr_regex = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')
        result = ip_addr_regex.search(public_ip_address).group()

        if result == public_ip_address:

            message = f'Your public ip address is {public_ip_address}.'

        else:
 
            message = "Couldn't connect to the server!"

    except:

        message = "Couldn't connect to the server!"

    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", message], text=True)

def cd_shred_logs(ghostsurf_logo_file_path, log_shredder_file_path, current_username):
    """A function which overrides the log files in the system"""

    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Shreading the log files."], text=True)
    sleep(0.3)
    run(["sudo", "-S", log_shredder_file_path, current_username], text=True, input=user_pwd)
    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Log shredding has been done."], text=True)

def cd_reset(user_pwd, ghostsurf_logo_file_path, reset_iptables_only_script_file_path, reset_script_file_path):
    """A function which resets the ghostsurf settings"""

    def reset_button_question_dialog_processor(i):
        """A function which process the input coming from the dialog box that is opened after the reset button is pressed to identify what app should do"""

        user_answer = i.text()
        sleep(0.3)

        if user_answer == "&Yes":

            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Resetting iptables rules only."], text=True)
            sleep(0.3)
            run(["sudo", "-S", reset_iptables_only_script_file_path], text=True, input=user_pwd)
            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Iptables rules are reset."], text=True)
 
        elif user_answer == "&No":

            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Resetting ghostsurf configurations."], text=True)
            sleep(0.3)
            run(["sudo", "-S", reset_script_file_path], text=True, input=user_pwd)
            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Reseting is done."], text=True)

        else:

            debug("Operation canceled")

    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("Do you want to reset iptables rules only?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.buttonClicked.connect(reset_button_question_dialog_processor)
    question_dialog.exec_()

def cd_change_mac_address(user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path):
    """A function which changes the mac address"""

    def mac_changer_button_question_dialog_processor(i):
        """A function which checks the user's answer for the mac changer question and instructs the computer about what to do based on that answer"""

        user_answer = i.text()

        if user_answer == "&Yes":

            mac_changer_thread = Thread(target=change_the_mac_address_and_connect_back_to_wifi, args=[user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path])
            mac_changer_thread.start()

        elif user_answer == "&No":

            run(["sudo", "-S", mac_changer_script_file_path], text=True, input=user_pwd)
            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Mac address has been changed."])

        else:

            debug("Operation canceled")

    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Changing the mac address."], text=True)

    sleep(0.3)
    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("Do you want to connect back to the internet?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog.buttonClicked.connect(mac_changer_button_question_dialog_processor)
    question_dialog.exec_()

def cd_wipe_memory(user_pwd, ghostsurf_logo_file_path, fast_bomb_script_file_path, secure_bomb_script_file_path):
    """A function which drops caches, wipes the memory securely and notifies the user"""

    def wipe_button_question_dialog_processor(i):
        """A function which process the input coming from the dialog box that is opened after the wipe button is pressed to identify what app should do"""
        
        user_answer = i.text()
        sleep(0.3)

        if user_answer == "&Yes":

            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Wiping the memory and droping caches. This might take some time!"], text=True)
            wipe_memory_thread = Thread(target=less_secure_memory_wipe, args=[user_pwd, ghostsurf_logo_file_path, fast_bomb_script_file_path])
            wipe_memory_thread.start()

        elif user_answer == "&No":

            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Wiping the memory and droping caches. This might take some time!"], text=True)
            wipe_memory_thread = Thread(target=high_secure_memory_wipe, args=[user_pwd, ghostsurf_logo_file_path, secure_bomb_script_file_path])
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

def cd_change_nameservers(user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path):
    """A function which changes the nameservers to enhance security and privacy"""

    run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Changing the nameservers."], text=True)
    sleep(0.3)
    thread = Thread(target=change_ns, args=[user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path])
    thread.start()

def cd_anonymize_browser(user_pwd, init_script_file_path, ghostsurf_logo_file_path, firefox_profiles_dir, custom_firefox_preferences_file_path, firefox_profiles_conf_file_path):
    """A function which anonymizes the firefox browser alread installed in the system."""

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

        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Creating Ghostsurf Firefox profile."], text=True)
        sleep(2)
        run(["firefox-esr", "-CreateProfile", "ghostsurf"], text=True)
        
        if custom_firefox_preferences_file_path.exists() == True:

            with open(custom_firefox_preferences_file_path, "r") as the_custom_prefs_file:
                custom_prefs = the_custom_prefs_file.read()

        else:

            run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Custom preferences file not found. Try to reinstall ghostsurf!"], text=True)

        ghostsurf_firefox_profile_file_path = next(Path(firefox_profiles_dir).glob("*.ghostsurf/user.js"))

        with open(ghostsurf_firefox_profile_file_path, "w") as ghostsurf_firefox_profile_user_pref_file:
            ghostsurf_firefox_profile_user_pref_file.write(custom_prefs)

        run(["sudo", "-S", init_script_file_path], text=True, input=user_pwd)

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

        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Ghostsurf Firefox profile has been created. And, preferences has been set."], text=True)

    else:

        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Ghostsurf Firefox profile already exists."], text=True)

    if is_penetration_testing_profile_exists == False:

        sleep(2)
        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Creating Penetration-Testing Firefox profile."], text=True)
        sleep(2)
        run(["firefox-esr", "-CreateProfile", "penetration-testing"], text=True)
        sleep(2)
        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Penetration-Testing Firefox profile has been created."], text=True)

    else:

        sleep(2)
        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "Penetration-Testing Firefox profile already exists."], text=True)

def cd_change_hostname(user_pwd, hostname_changer_script_file_path):
    """A function changing device's hostname."""

    question_dialog = QMessageBox()
    question_dialog.setIcon(QMessageBox.Question)
    question_dialog.setWindowTitle("Important")
    question_dialog.setText("This operation requires reboot. Do you allow to reboot this system?")
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    question_dialog_answer = question_dialog.exec()

    if question_dialog_answer == QMessageBox.Yes:

        debug("Rebooting the system")
        run(["sudo", "-S", hostname_changer_script_file_path], text=True, input=user_pwd)
        run(["sudo", "-S", "reboot"], text=True, input=user_pwd)

    else:

        debug("Operation canceled")