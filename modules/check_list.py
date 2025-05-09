# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from socket import gethostname
from subprocess import run
from pathlib import Path

# Ghostsurf Modules
from modules.json_config_loading import (
    load_ghostsurf_config,
    save_ghostsurf_config,
)
from modules.logging_config import (
    debug,
    info,
    warning,
    error,
)



##############################

# CHECK LIST FUNCTIONS

##############################

def check_fake_hostname_usage(fake_hostnames_list_file_path, checklist_items_dict):
    with open(fake_hostnames_list_file_path, "r") as fake_hostnames_file:
        list_of_fake_hostnames = fake_hostnames_file.readlines()
    current_hostname = gethostname()

    if f'{current_hostname}\n' in list_of_fake_hostnames:
        checklist_items_dict['Using fake hostname'] = True
    else:
        checklist_items_dict['Using fake hostname'] = False

def check_fake_mac_address_usage(checklist_items_dict):
    list_of_network_interfaces = run(
        ["ip -o link show | awk -F': ' '{print $2}'"],
        shell=True,
        text=True,
        capture_output=True
    ).stdout.strip("\n\r").split("\n")
    verification_list = []

    for interface in list_of_network_interfaces:
        interface = interface.strip("\n\r")

        if interface != "lo":
            debug(f"Network Interface Name = {interface}")
            mac_address_info = run(
                ["macchanger", "-s", interface],
                capture_output=True,
                text=True
            ).stdout.split("\n")[:-1]
            permanent_mac_address = mac_address_info[1].split(" ")[2].strip()
            current_mac_address = mac_address_info[0].split(" ")[4].strip()
            debug(f'Permanent Mac Address = {permanent_mac_address}\nCurrent Mac Address = {current_mac_address}')

            if current_mac_address != permanent_mac_address:
                verification_list.append(True)
                if verification_list.count(True) == len(list_of_network_interfaces) -1:
                    checklist_items_dict['Using fake mac address'] = True
                else:
                    checklist_items_dict['Using fake mac address'] = False
            else:
                verification_list.append(False)
                checklist_items_dict['Using fake mac address'] = False

def check_appropriate_nameserver_usage(
    privacy_focused_nameservers_file_path,
    original_resolv_configuration_file_path,
    checklist_items_dict,
    ghostsurf_settings_file_path
):
    with open(privacy_focused_nameservers_file_path, "r") as privacy_focused_nameservers_file:
        privacy_focused_nameservers = privacy_focused_nameservers_file.read().strip('\n\r')
    tor_nameserver = "nameserver 127.0.0.1"
    with open(original_resolv_configuration_file_path, "r") as resolv_conf_file:
        resolv_conf_file_contents = resolv_conf_file.read().strip('\n\r')
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    debug(f'Is transparent proxy on = {config["is_ghostsurf_on"]}')
    debug(
        f'Privacy Focused Nameservers = {privacy_focused_nameservers}\n'
        f'Resolv.conf File = {resolv_conf_file_contents}\n'
        f'Tor Nameserver = {tor_nameserver}'
    )

    if config["is_ghostsurf_on"] == "False":
        if resolv_conf_file_contents == privacy_focused_nameservers:
            checklist_items_dict['Using appropriate nameservers'] = True
        else:
            checklist_items_dict['Using appropriate nameservers'] = False
    else:
        if resolv_conf_file_contents == tor_nameserver:
            checklist_items_dict['Using appropriate nameservers'] = True
        else:
            checklist_items_dict['Using appropriate nameservers'] = False

def check_browser_anonymization(
    current_username,
    checklist_items_dict,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path
):
    ghostsurf_firefox_profile_dir_glob = list(Path(firefox_profiles_dir).glob("*.ghostsurf"))
    debug(f"Ghostsurf Firefox profile dir glob = {ghostsurf_firefox_profile_dir_glob}")

    if ghostsurf_firefox_profile_dir_glob:
        ghostsurf_firefox_profile_dir = ghostsurf_firefox_profile_dir_glob[0]
        debug(f"Ghostsurf Firefox profile dir path = {ghostsurf_firefox_profile_dir}")
        # Construct the path to user.js
        ghostsurf_firefox_profile_file_path = Path(ghostsurf_firefox_profile_dir, "user.js")
        debug(f"Ghostsurf Firefox profile file path = {ghostsurf_firefox_profile_file_path}")

    penetration_testing_firefox_profile_file_path_glob = list(Path(firefox_profiles_dir).glob("*.penetration-testing"))

    if penetration_testing_firefox_profile_file_path_glob:
        penetration_testing_firefox_profile_file_path = penetration_testing_firefox_profile_file_path_glob[0]

    if (
        'ghostsurf_firefox_profile_file_path' in locals() and 
        ghostsurf_firefox_profile_file_path.exists() and
        custom_firefox_preferences_file_path.exists() and
        penetration_testing_firefox_profile_file_path_glob and
        penetration_testing_firefox_profile_file_path.exists()
    ):
        with open(custom_firefox_preferences_file_path, "r") as cfpfp:
            cfpfp_contents = cfpfp.read()
        with open(ghostsurf_firefox_profile_file_path, "r") as gfpfp:
            gfpfp_contents = gfpfp.read()
        debug(f'''Custom Firefox Preferences File Path Content = {cfpfp_contents}
            Ghostsurf Firefox Profile File Path Content = {gfpfp_contents}''')
        checklist_items_dict[
            'Ghostsurf\'s Firefox profiles are available. And, preferences are set'
        ] = bool(
            cfpfp_contents == gfpfp_contents
        )
    else:
        debug('Couldn\'t find a path')

def check_different_timezone_usage(timezone_backup_file_path, checklist_items_dict):
    with open(timezone_backup_file_path, "r") as original_timezone_file:
        otf_content = original_timezone_file.read().strip()
    current_timezone = run(
        ["timedatectl show | grep Timezone | sed 's/Timezone=//g'"],
        shell=True,
        capture_output=True,
        text=True
    ).stdout.strip()
    is_timezone_different = bool(otf_content!=current_timezone)
    debug(f'''Original Timezone = {otf_content}
        Current Timezone = {current_timezone}
        Is Timezone Different = {is_timezone_different}''')
    checklist_items_dict['Using different timezone'] = is_timezone_different

def check_tor_connection_usage(checklist_items_dict):
    tor_connection_command = (
        "curl -s https://check.torproject.org/ | "
        "grep -q Congratulations && echo 'Connected through Tor' || "
        "echo 'Not connected through Tor'"
    )
    tor_connection_status = run(
        tor_connection_command,
        shell=True,
        capture_output=True,
        text=True
    ).stdout.strip()
    is_transparent_proxy_set_correctly = bool(tor_connection_status=="Connected through Tor")
    debug(
        f"Check Tor Project Result = {tor_connection_status}\n"
        f"Is Transparent Proxy Set Correctly = {is_transparent_proxy_set_correctly}"
    )
    checklist_items_dict['Using a tor connection'] = is_transparent_proxy_set_correctly