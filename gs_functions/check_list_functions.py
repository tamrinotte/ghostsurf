# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from socket import gethostname
from subprocess import run
from os import popen
from pathlib import Path



# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)



##############################

# CHECK LIST FUNCTIONS

##############################

def check_fake_hostname_usage(fake_hostnames_list_file_path, checklist_items_dict):
    """A function which checks the hostname"""

    # Opening the list_of_fake_hostnames file in reading mode 
    with open(fake_hostnames_list_file_path, "r") as fake_hostnames_file:

        # Creating a list of fake hostnames from the fake_hostnames_file's lines
        list_of_fake_hostnames = fake_hostnames_file.readlines()

    # Getting the current hostname
    current_hostname = gethostname()

    # Checking if the current hostname is in the list of fake hostnames
    if f'{current_hostname}\n' in list_of_fake_hostnames:

        # Updating the 'Using fake hostname' key's value pair to True
        checklist_items_dict['Using fake hostname'] = True

def check_fake_mac_address_usage(user_pwd, checklist_items_dict):
    """A function which checks wheather or not you are using fake mac address"""

    # Getting the active network adaptor's name
    list_of_network_interfaces = run(["sudo", "-S",  "bash", "-c", "ip -o link show | awk -F': ' '{print $2}'"], input=user_pwd, text=True, capture_output=True).stdout.strip("\n\r").split("\n")

    verification_list = []

    for interface in list_of_network_interfaces:

        interface = interface.strip("\n\r")

        if interface != "lo":

            debug(f"Network Interface Name = {interface}")

            # Getting mac address information
            mac_address_info = popen(f'macchanger -s {interface}').read().split("\n")[:-1]

            # Getting the permanent mac address
            permanent_mac_address = mac_address_info[1].split(" ")[2].strip()

            # Getting the current mac address
            current_mac_address = mac_address_info[0].split(" ")[4].strip()

            # Printing the permanent mac address and the current mac address in debug mode.
            debug(f'Permanent Mac Address = {permanent_mac_address}\nCurrent Mac Address = {current_mac_address}')

            # Checking if the current mac address is not equal to the permanent mac address
            if current_mac_address != permanent_mac_address:

                verification_list.append(True)

                if verification_list.count(True) == len(list_of_network_interfaces) -1:

                    # Setting the 'Using fake mac address' key's value pair to True
                    checklist_items_dict['Using fake mac address'] = True

                else:

                    # Setting the 'Using fake mac address' key's value pair to False
                    checklist_items_dict['Using fake mac address'] = False

            else:

                verification_list.append(False)

                # Setting the 'Using fake mac address' key's value pair to False
                checklist_items_dict['Using fake mac address'] = False

def check_appropriate_nameserver_usage(privacy_focused_nameservers_file_path, original_resolv_configuration_file_path, main_window, checklist_items_dict):
    """A function which checks if you are using privacy focused name servers"""

    # Opening the privacy_focused_nameservers_resolv.conf file in reading mode as privacy_focused_nameservers_file
    with open(privacy_focused_nameservers_file_path, "r") as privacy_focused_nameservers_file:

        # Reading privacy_focused_nameservers_file's lines
        privacy_focused_nameservers = privacy_focused_nameservers_file.read().strip('\n\r')

    # Creating a variable that holds the tor nameserver specification 
    tor_nameserver = "nameserver 127.0.0.1"

    # Opening the resolv.conf file in reading mode as resolv_conf_file
    with open(original_resolv_configuration_file_path, "r") as resolv_conf_file:

        # Reading resolv_conf_file's contents
        resolv_conf_file_contents = resolv_conf_file.read().strip('\n\r')

    debug(f'Start stop button\'s text = {main_window.start_stop_button.text()}')

    debug(f'Privacy Focused Nameservers = {privacy_focused_nameservers}\nResolv.conf File = {resolv_conf_file_contents}\nTor Nameserver = {tor_nameserver}')

    # Checking if start_stop_button's text in the main window is equal to Start string.
    if main_window.start_stop_button.text() == "Start":

        # Checking if resolv_conf_file_contents is equal to privacy_focused_nameservers
        if resolv_conf_file_contents == privacy_focused_nameservers:

            # Setting the 'Using appropriate nameservers' key's value pair to True
            checklist_items_dict['Using appropriate nameservers'] = True

    # Checking if start_stop_button's text in the main window is not equal to Start string.
    else:

        if resolv_conf_file_contents == tor_nameserver:

            # Setting the 'Using appropriate nameservers' key's value pair to True
            checklist_items_dict['Using appropriate nameservers'] = True

def check_browser_anonymization(current_username, checklist_items_dict, custom_firefox_preferences_file_path):
    """A function which checks if browser anonymization preferences are in use"""

    ghostsurf_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.ghostsurf".format(current_username)], text=True, capture_output=True).stdout.strip(), "user.js")
    
    penetration_testing_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.penetration-testing".format(current_username)], text=True, capture_output=True).stdout.strip())

    if ghostsurf_firefox_profile_file_path.exists() == True and custom_firefox_preferences_file_path.exists() == True and penetration_testing_firefox_profile_file_path.exists() == True:

        with open(custom_firefox_preferences_file_path, "r") as cfpfp:

            cfpfp_contents = cfpfp.read()

        with open(ghostsurf_firefox_profile_file_path, "r") as gfpfp:

            gfpfp_contents = gfpfp.read()

        debug(f'Custom Firefox Preferences File Path Content = {cfpfp_contents}\nGhostsurf Firefox Profile File Path Content = {gfpfp_contents}')
        
        # Setting the 'Ghostsurf\'s Firefox profiles are available. And, preferences are set' key's value pair to True
        checklist_items_dict['Ghostsurf\'s Firefox profiles are available. And, preferences are set'] = bool(cfpfp_contents == gfpfp_contents)

    else:

        debug('Couldn\'t find a path')

def check_different_timezone_usage(timezone_backup_file_path, checklist_items_dict):
    """A function which checks if a different timezone is set in the system"""

    # Opening the file in timezone_backup_file_path in reading mode with original_timezone_file name
    with open(timezone_backup_file_path, "r") as original_timezone_file:

        # Reading the file's contents
        otf_content = original_timezone_file.read().strip()

    # Getting the current timezone using system commands
    current_timezone = popen("timedatectl show | grep Timezone | sed 's/Timezone=//g'").read().strip()

    # Creating a boolean by checking if otf_content is not equal to current_timezone
    is_timezone_different = bool(otf_content!=current_timezone)
    
    # Printing the original timezone, current time zone and the is_timezone_different variable's value in debug mode
    debug(f'Original Timezone = {otf_content}\nCurrent Timezone = {current_timezone}\nIs Timezone Different = {is_timezone_different}')

    # Setting the 'Using different timezone' key's value pair to True
    checklist_items_dict['Using different timezone'] = is_timezone_different

def check_tor_connection_usage(checklist_items_dict):
    """A function which checks if a transparent proxy is working."""

    # Sending a get request to https://check.torproject.org to learn if transparent proxy set correctly
    tor_connection_status = str(popen(f'curl -s https://check.torproject.org/ | grep -q Congratulations && echo "Connected through Tor" || echo "Not connected through Tor"').read()).strip()

    # Creaing a boolean
    is_transparent_proxy_set_correctly = bool(tor_connection_status=="Connected through Tor")

    # Printing if transparent proxy set correctly in debug mode
    debug(f'Check Tor Project Result = {tor_connection_status}\nIs Transparent Proxy Set Correctly = {is_transparent_proxy_set_correctly}')

    # Setting the 'Using different timezone' key's value pair to True
    checklist_items_dict['Using a tor connection'] = is_transparent_proxy_set_correctly