# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import socket
import subprocess
import pathlib
import requests
import requests.exceptions

# Ghostsurf Modules
from modules.conf_logging import (
    debug,
    info,
    warning,
    error,
)
from modules.conf_ghostsurf import (
    load_ghostsurf_config,
    save_ghostsurf_config,
)

##############################

# FAKE HOSTNAME

##############################

def check_fake_hostname_usage(fake_hostnames_list_file_path, checklist_items_dict):
    try:
        if not fake_hostnames_list_file_path.is_file():
            warning(f"Fake hostname list file not found: {fake_hostnames_list_file_path}")
            checklist_items_dict['Using fake hostname'] = False
            return

        with open(fake_hostnames_list_file_path, "r", encoding="utf-8") as file:
            fake_hostnames = {line.strip() for line in file if line.strip()}

        current_hostname = socket.gethostname().strip()
        is_using_fake = current_hostname in fake_hostnames
        checklist_items_dict['Using fake hostname'] = is_using_fake
        debug(f"Current hostname: {current_hostname}")
        debug(f"Using fake hostname: {is_using_fake}")

    except Exception as e:
        error(f"Exception occurred while checking fake hostname usage: {e}")
        checklist_items_dict['Using fake hostname'] = False

##############################

# FAKE MAC ADDRESS

##############################

def check_fake_mac_address_usage(checklist_items_dict):
    try:
        is_fake_mac_used = False
        verification_list = []
        raw_list_of_network_interfaces = subprocess.run(
            ["ip -o link show | awk -F': ' '{print $2}'"],
            shell=True,
            text=True,
            capture_output=True
        ).stdout.strip("\n\r").split("\n")

        for interface in raw_list_of_network_interfaces:
            interface = interface.strip("\n\r")
            if interface != "lo":
                debug(f"Network Interface Name = {interface}")
                mac_address_info = subprocess.run(
                    ["macchanger", "-s", interface],
                    capture_output=True,
                    text=True
                ).stdout.split("\n")[:-1]
                permanent_mac_address = mac_address_info[1].split(" ")[2].strip()
                current_mac_address = mac_address_info[0].split(" ")[4].strip()
                debug(f'Permanent Mac Address = {permanent_mac_address} - Current Mac Address = {current_mac_address}')
                if current_mac_address != permanent_mac_address:
                    verification_list.append(True)
                else:
                    verification_list.append(False)
      
        if verification_list.count(True) == len(raw_list_of_network_interfaces) -1: # -1 is for "lo"
            checklist_items_dict['Using fake mac address'] = True
        else:
            checklist_items_dict['Using fake mac address'] = False

    except Exception as e:
        error(f"Unexpected error during MAC address check: {e}")
        checklist_items_dict['Using fake mac address'] = False

##############################

# NAMESERVERS

##############################

def check_appropriate_nameserver_usage(
    privacy_focused_nameservers_file_path,
    original_resolv_configuration_file_path,
    checklist_items_dict,
    ghostsurf_settings_file_path
):
    try:
        # Check if the required files exist
        if not pathlib.Path(privacy_focused_nameservers_file_path).is_file():
            warning(f"Privacy nameserver list file not found: {privacy_focused_nameservers_file_path}")
            checklist_items_dict['Using appropriate nameservers'] = False
            return

        if not pathlib.Path(original_resolv_configuration_file_path).is_file():
            warning(f"Resolv.conf file not found: {original_resolv_configuration_file_path}")
            checklist_items_dict['Using appropriate nameservers'] = False
            return

        # Read expected values
        with open(privacy_focused_nameservers_file_path, "r", encoding="utf-8") as file:
            privacy_nameservers = "\n".join(
                line.strip() for line in file.readlines() if line.strip()
            )

        with open(original_resolv_configuration_file_path, "r", encoding="utf-8") as file:
            current_nameservers = "\n".join(
                line.strip() for line in file.readlines() if line.strip()
            )

        tor_nameserver = "nameserver 127.0.0.1"
        config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
        is_transparent_proxy_on = config.get("is_ghostsurf_on", "False")

        # Logging for traceability
        debug(f'Ghostsurf Transparent Proxy Enabled: {is_transparent_proxy_on}')
        debug(f'Expected Privacy Nameservers: {privacy_nameservers}')
        debug(f'Current resolv.conf Contents: {current_nameservers}')
        debug(f'Tor Nameserver: {tor_nameserver}')

        # Check appropriate configuration
        if is_transparent_proxy_on == "False":
            checklist_items_dict['Using appropriate nameservers'] = (
                current_nameservers == privacy_nameservers
            )
        else:
            checklist_items_dict['Using appropriate nameservers'] = (
                current_nameservers == tor_nameserver
            )

        debug(f"Using appropriate nameservers: {checklist_items_dict['Using appropriate nameservers']}")

    except Exception as e:
        error(f"Error while checking nameserver usage: {e}")
        checklist_items_dict['Using appropriate nameservers'] = False

##############################

# BROWSER ANONYMIZATION

##############################

def check_browser_anonymization(
    current_username,
    checklist_items_dict,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path
):
    checklist_key = "Ghostsurf's Firefox profiles are available. And, preferences are set"
    checklist_items_dict[checklist_key] = False  # Default to False unless everything matches

    try:
        # Look for Ghostsurf and Penetration Testing Firefox profiles
        ghostsurf_profile_dirs = list(pathlib.Path(firefox_profiles_dir).glob("*.ghostsurf"))
        pentest_profile_dirs = list(pathlib.Path(firefox_profiles_dir).glob("*.penetration-testing"))

        debug(f"Ghostsurf Firefox profile dirs found: {ghostsurf_profile_dirs}")
        debug(f"Penetration Testing Firefox profile dirs found: {pentest_profile_dirs}")

        if not ghostsurf_profile_dirs:
            warning("No Ghostsurf Firefox profile directory found.")
            return

        if not pentest_profile_dirs:
            warning("No Penetration Testing Firefox profile directory found.")
            return

        ghostsurf_profile_path = ghostsurf_profile_dirs[0]
        pentest_profile_path = pentest_profile_dirs[0]

        ghostsurf_user_js_path = ghostsurf_profile_path / "user.js"
        debug(f"Ghostsurf user.js path: {ghostsurf_user_js_path}")

        # Check that all required files exist
        if not ghostsurf_user_js_path.exists():
            warning(f"user.js not found in Ghostsurf profile: {ghostsurf_user_js_path}")
            return

        if not custom_firefox_preferences_file_path.exists():
            warning(f"Custom Firefox preferences file not found: {custom_firefox_preferences_file_path}")
            return

        # Read file contents
        with open(custom_firefox_preferences_file_path, "r", encoding="utf-8") as f:
            custom_prefs = f.read().strip()

        with open(ghostsurf_user_js_path, "r", encoding="utf-8") as f:
            ghostsurf_prefs = f.read().strip()

        debug("Comparing custom preferences with Ghostsurf profile user.js")
        debug(f"Custom prefs content:\n{custom_prefs}")
        debug(f"Ghostsurf prefs content:\n{ghostsurf_prefs}")

        # Compare contents strictly
        checklist_items_dict[checklist_key] = (custom_prefs == ghostsurf_prefs)

    except Exception as e:
        error(f"Exception occurred while checking browser anonymization: {e}")

##############################

# TIME ZONE

##############################

def check_different_timezone_usage(timezone_backup_file_path, checklist_items_dict):
    try:
        if not timezone_backup_file_path.is_file():
            debug(f"Timezone backup file not found: {timezone_backup_file_path}")
            checklist_items_dict['Using different timezone'] = False
            return

        original_timezone = timezone_backup_file_path.read_text(encoding="utf-8").strip()
        current_timezone = subprocess.run(
            ["timedatectl", "show", "-p", "Timezone", "--value"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        is_timezone_different = (original_timezone != current_timezone)

        debug(
            f"Original Timezone = {original_timezone}\n"
            f"Current Timezone = {current_timezone}\n"
            f"Is Timezone Different = {is_timezone_different}"
        )

        checklist_items_dict['Using different timezone'] = is_timezone_different

    except FileNotFoundError:
        error(f"Timezone backup file does not exist: {timezone_backup_file_path}")
        checklist_items_dict['Using different timezone'] = False
    except Exception as e:
        error(f"Unexpected error in timezone check: {e}")
        checklist_items_dict['Using different timezone'] = False

##############################

# TOR CONNECTION

##############################

def check_tor_connection_usage(checklist_items_dict):
    url = "https://check.torproject.org/"
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "curl"})
        response.raise_for_status()
        content = response.text

        is_connected = ("Congratulations" in content)

        debug(
            f"Check Tor Project page fetched successfully.\n"
            f"Is Connected Through Tor = {is_connected}"
        )

        checklist_items_dict['Using a tor connection'] = is_connected

    except requests.exceptions.Timeout:
        error("Timeout occurred while trying to connect to Tor check site.")
        checklist_items_dict['Using a tor connection'] = False
    except requests.exceptions.RequestException as e:
        error(f"Network error while checking Tor connection: {e}")
        checklist_items_dict['Using a tor connection'] = False
    except Exception as e:
        error(f"Unexpected error during Tor connection check: {e}")
        checklist_items_dict['Using a tor connection'] = False