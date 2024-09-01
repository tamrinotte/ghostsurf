# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from re import compile
from time import sleep
from pathlib import Path
from webbrowser import open as wbopen
from subprocess import run
from getpass import getpass

# Ghostsurf Modules
from modules.check_list import (
    check_fake_hostname_usage, 
    check_fake_mac_address_usage, 
    check_appropriate_nameserver_usage, 
    check_browser_anonymization,
    check_different_timezone_usage,
    check_tor_connection_usage,
)

from modules.standard import (
    load_ghostsurf_config,
    save_ghostsurf_config,
)


# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)



##############################

# TEXT BASED UI FUNCTIONS

##############################

def tui_start_transparent_proxy(init_script_file_path, start_transparent_proxy_script_file_path, ghostsurf_settings_file_path):
    """A function starting transparent proxy."""

    debug("Start command has been entered. Starting transparent proxy.")

    while True:

        question = str(input("Are you allowing to killing of dangerous applications and cleaning of dangerous caches? (y/n) ")).strip().lower()

        if question == "y" or question == "yes":
            
            script = f"bash {init_script_file_path} && bash {start_transparent_proxy_script_file_path}"
            run(["pkexec", "bash", "-c", script], text=True)
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
            config["is_ghostsurf_on"] = "True"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            print("Ghostsurf has been turned on.")
            break

        elif question == "n" or question == "no":

            run(["pkexec", start_transparent_proxy_script_file_path], text=True)
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
            config["is_ghostsurf_on"] = "True"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            print("Ghostsurf has been turned on.")
            break

        else:

            print("That's not a valid answer.")

def tui_stop_transparent_proxy(init_script_file_path, stop_transparent_proxy_script_file_path, ghostsurf_settings_file_path):
    """A function stopping transparent proxy."""

    debug("Stop command has been entered. Stopping transparent proxy.")

    while True:

        question = str(input("Are you allowing to killing of dangerous applications and cleaning of dangerous caches? (y/n) ")).strip().lower()

        if question == "y" or question == "yes":

            script = f"bash {init_script_file_path} && bash {stop_transparent_proxy_script_file_path}"
            run(["pkexec", "bash", "-c", script], text=True)
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
            config["is_ghostsurf_on"] = "False"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            print("Ghostsurf has been turned off.")
            break

        elif question == "n" or question == "no":

            run(["pkexec", stop_transparent_proxy_script_file_path], text=True)
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
            config["is_ghostsurf_on"] = "False"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            print("Ghostsurf has been turned off.")
            break

        else:

            print("That's not a valid answer.")

def tui_change_ip():
    """A function restarting tor service to change devices public IP address."""

    debug("Change command has been entered. Restarting the tor service.")
    run(["pkexec", "systemctl", "restart", "tor"], text=True)
    print("Your public IP address has been changed, you can type \"myip\" to see your new IP address.")

def tui_show_ip():
    """A function displaying device's public IP address."""

    debug("Myip command has been entered. Trying to display device's public ip address.")

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

    print(message)

def tui_show_status(ghostsurf_settings_file_path):
    """A function displaying if transparent proxy is on/off."""

    debug("Status command has been entered. Trying to display ghostsurf working status.")
    status_dict = {
        "Is Ghostsurf ON": False,
        "Is Ghostsurf Enabled at Boot": False,
        "Is Tor Service Active": False,
    }

    tor_service_status = run(["pkexec", "systemctl", "status", "tor"], capture_output=True, text=True).stdout.strip()

    if "inactive" in tor_service_status:

        status_dict["Is Tor Service Active"] = True

    else:

        status_dict["Is Tor Service Active"] = False

    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)

    if config["is_ghostsurf_on"] == "True":

        status_dict["Is Ghostsurf ON"] = True

    else:

        status_dict["Is Ghostsurf ON"] = False

    if config["is_enabled_at_boot"] == "True":

        status_dict["Is Ghostsurf Enabled at Boot"] = True

    else:

        status_dict["Is Ghostsurf Enabled at Boot"] = False

    for k,v in status_dict.items():

        print(f'{k} = {v}')


def tui_change_mac_address(mac_changer_script_file_path):
    """A function changing device's mac address."""

    debug("Changemac command has been entered. Trying to change the mac address.")

    while True:

        question = str(input("Do you want to connect back to the internet? (y/n) ")).strip().lower()

        if question == "y" or question == "yes":

            debug("Trying to change the mac address and trying to connect back to the internet.")
            internet_adaptor_name = run(["ip route show default | awk '/default/ {print $5}'"], shell=True, capture_output=True, text=True).stdout.strip()
            script = f"bash {mac_changer_script_file_path} && sleep 4 && nmcli d connect {internet_adaptor_name}"
            run(["pkexec", "bash", "-c", script], text=True)
            print("MAC address has been changed.")
            break

        elif question == "n" or question == "no":

            debug("Trying to change the mac address.")
            run(["pkexec", mac_changer_script_file_path], text=True)
            print("MAC address has been changed.")
            break

        else:

            print("That's not a valid answer.")

def tui_change_dns(nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path, ghostsurf_settings_file_path):
    """A function changing domain name servers."""

    debug("Changedns command has been entered. Trying to change the DNS.")
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)

    if config["is_ghostsurf_on"] == "True":

        script = f"bash {nameserver_changer_file_path} {tor_nameservers_file_path} && cp {tor_nameservers_file_path} {original_resolv_configuration_file_path}"
        run(["pkexec", "bash", "-c", script], text=True)
        print("Nameservers has been changed.")

    else:

        script = f"bash {nameserver_changer_file_path} {privacy_focused_nameservers_file_path} && cp {privacy_focused_nameservers_file_path} {original_resolv_configuration_file_path}"
        run(["pkexec", "bash", "-c", script], text=True)
        print("Nameservers has been changed.")

def tui_change_hostname(hostname_changer_script_file_path):
    """A function which changes device's hostname."""

    debug("Changemyhostname command has been entered. Trying to change the hostname.")

    while True:

        question = str(input("This operation requires system reboot. Are you allowing to a system reboot? (y/n) ")).strip().lower()

        if (question == "y" or question == "yes"):

            debug("Rebooting the system")
            script = f"bash {hostname_changer_script_file_path} && reboot"
            run(["pkexec", "bash", "-c", script], text=True)
            break

        elif (question == "n" or question == "no"):

            print("Canceling the operation.")
            break

        else:

            print("That's not a valid answer.")

def tui_display_the_help_page(url):
    """A function opening the README.md file of this application."""

    wbopen(url)
    print("Help page has been opened in your default browser.")


def tui_wipe_memory(fast_bomb_script_file_path, secure_bomb_script_file_path):
    """A function rendering the memory."""

    while True:

        question = str(input("Do you want fast and less secure operation? (y/n)")).lower().strip()

        if question == "y" or question == "yes":

            run(["pkexec", fast_bomb_script_file_path], text=True)
            print("Memory has been wiped.")
            break

        elif question == "n" or question == "no":

            run(["pkexec", secure_bomb_script_file_path], text=True)
            print("Memory has been wiped.")
            break

        else:

            print("That's not a valid answer.")

def tui_anonymize_browser(firefox_profiles_dir, custom_firefox_preferences_file_path, init_script_file_path, firefox_profiles_conf_file_path):
    """A function which anonymizes firefox by changing it's preferences"""
    
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
    
        run(["firefox-esr", "-CreateProfile", "ghostsurf"], text=True)

        if Path(custom_firefox_preferences_file_path).exists() == True:

            with open(custom_firefox_preferences_file_path, "r") as the_custom_prefs_file:
                custom_prefs = the_custom_prefs_file.read()

        else:

            print("Custom preferences file not found. Try to reinstall ghostsurf!")

        ghostsurf_firefox_profile_file_path = str(next(Path(firefox_profiles_dir).glob("*.ghostsurf/user.js")))

        with open(ghostsurf_firefox_profile_file_path, "w") as ghostsurf_firefox_profile_user_pref_file:
            ghostsurf_firefox_profile_user_pref_file.write(custom_prefs)

        run(["pkexec", init_script_file_path], text=True)

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

        print("Ghostsurf Firefox profile has been created. And, preferences has been set.")

    else:
        
        print(f"Ghostsurf Firefox profile already exists.")

    if is_penetration_testing_profile_exists == False:

        run(["firefox-esr", "-CreateProfile", "penetration-testing"], text=True)
        print("Penetration-Testing Firefox profile has been created.")

    else:

        print(f"Penetration-Testing Firefox profile already exists.")

def tui_shred_logs(log_shredder_file_path, current_username):
    """A function which overrides the log files in the system"""

    run("pkexec", log_shredder_file_path, current_username)
    print("Log files has been shredded!")

def tui_checklist(fake_hostnames_list_file_path, privacy_focused_nameservers_file_path, original_resolv_configuration_file_path, current_username, firefox_profiles_dir, custom_firefox_preferences_file_path, timezone_backup_file_path, ghostsurf_settings_file_path):
    """A function running a checklist decrease blunders."""

    checklist_items_dict = {
        'Using fake hostname': False,
        'Using fake mac address': False,
        'Using appropriate nameservers': False,
        'Ghostsurf\'s Firefox profiles are available. And, preferences are set': False,
        'Using different timezone': False,
        'Using a tor connection': False,
        'Using man in the middle protection': False
    }

    check_fake_hostname_usage(fake_hostnames_list_file_path=fake_hostnames_list_file_path, checklist_items_dict=checklist_items_dict)
    check_fake_mac_address_usage(checklist_items_dict=checklist_items_dict)
    check_appropriate_nameserver_usage(privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path, original_resolv_configuration_file_path=original_resolv_configuration_file_path, checklist_items_dict=checklist_items_dict, ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    check_browser_anonymization(current_username=current_username, checklist_items_dict=checklist_items_dict, firefox_profiles_dir=firefox_profiles_dir, custom_firefox_preferences_file_path=custom_firefox_preferences_file_path)
    check_different_timezone_usage(timezone_backup_file_path=timezone_backup_file_path, checklist_items_dict=checklist_items_dict)
    check_tor_connection_usage(checklist_items_dict=checklist_items_dict)

    print("Anonymity Checklist")
    for k, v in checklist_items_dict.items():
        print(f"{k} = {v}")

def tui_reset(reset_iptables_only_script_file_path, reset_script_file_path):
    """A function resetting ghostsurf adjustments."""

    while True:

        question = str(input("Do you want to reset iptables rules only? (y/n) ")).lower().strip()

        if question == "y" or question == "yes":

            run(["pkexec", reset_iptables_only_script_file_path], text=True)
            print("Iptables rules has been resetted.")
            break

        elif question =="n" or question == "no":

            run(["pkexec", reset_script_file_path], text=True)
            print("Ghostsurf changes has been reset.")
            break

        else:

            print("That's not a valid answer.")

def tui_enable_at_boot(start_transparent_proxy_script_file_path, save_iptables_script_file_path, ghostsurf_settings_file_path):
    """A function enabling ghostsurf to start automatically at boot."""

    script = f"bash {start_transparent_proxy_script_file_path} && bash {save_iptables_script_file_path}"
    run(["pkexec", "bash", "-c", script], text=True)
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    config["is_enabled_at_boot"] = "True"
    save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    config["is_ghostsurf_on"] = "True"
    save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
    print("Ghostsurf has been enabled and turned on.")

def tui_disable_at_boot(stop_transparent_proxy_script_file_path, save_iptables_script_file_path, ghostsurf_settings_file_path):
    """A function disabling ghostsurf to start automatically at boot."""
    
    script = f"bash {stop_transparent_proxy_script_file_path} && bash {save_iptables_script_file_path}"
    run(["pkexec", "bash", "-c", script], text=True)
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    config["is_enabled_at_boot"] = "False"
    save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    config["is_ghostsurf_on"] = "False"
    save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
    print("Ghostsurf has been disabled and turned off.")