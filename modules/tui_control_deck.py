# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from webbrowser import open as wbopen

# Ghostsurf Modules
from modules.conf_ghostsurf import (
    load_ghostsurf_config,
)
from modules.conf_notification import display_notification
from modules.conf_dialog import ask_confirmation
from modules.ops_network import (
    get_public_ip_address,
    change_public_ip_address,
    change_mac_address,
    change_nameservers,
    get_tor_status,
    get_proxy_status,
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
)
from modules.ops_checklist import (
    check_fake_hostname_usage, 
    check_fake_mac_address_usage, 
    check_appropriate_nameserver_usage, 
    check_browser_anonymization,
    check_different_timezone_usage,
    check_tor_connection_usage,
)

##############################

# GLOBAL VARIABLES

##############################

is_using_gui = False

##############################

# START TRANSPARENT PROXY

##############################

def tui_cd_start_transparent_proxy(
    init_script_file_path,
    start_transparent_proxy_script_file_path,
    ghostsurf_settings_file_path
):
    allow_cleanup = ask_confirmation(
        "Do you allow the termination of dangerous applications and cleaning of dangerous caches? (y/n): "
    )
    start_proxy(
        init_script_file_path=init_script_file_path,
        start_transparent_proxy_script_file_path=start_transparent_proxy_script_file_path,
        is_positive=allow_cleanup,
        ghostsurf_settings_file_path=ghostsurf_settings_file_path,
        is_using_gui=is_using_gui,
    )

##############################

# STOP TRANSPARENT PROXY

##############################

def tui_cd_stop_transparent_proxy(
    init_script_file_path,
    stop_transparent_proxy_script_file_path,
    ghostsurf_settings_file_path
):
    allow_cleanup = ask_confirmation(
        "Do you allow the termination of dangerous applications and cleaning of dangerous caches? (y/n): "
    )
    stop_proxy(
        init_script_file_path=init_script_file_path,
        stop_transparent_proxy_script_file_path=stop_transparent_proxy_script_file_path,
        is_positive=allow_cleanup,
        ghostsurf_settings_file_path=ghostsurf_settings_file_path,
        is_using_gui=is_using_gui,
    )

##############################

# CHANGING DEVICES IP ADDRESS

##############################

def tui_cd_change_ip():
    change_public_ip_address(is_using_gui=is_using_gui)

##############################

# DISPLAYING THE PUBLIC IP ADDRESS

##############################

def tui_cd_show_ip():
    get_public_ip_address(is_using_gui=is_using_gui)

##############################

# SHOWING CONNECTION STATUS

##############################

def tui_cd_show_status(ghostsurf_settings_file_path):
    get_tor_status(
        is_using_gui=is_using_gui
    )
    get_proxy_status(
        ghostsurf_settings_file_path=ghostsurf_settings_file_path,
        is_using_gui=is_using_gui
    )

##############################

# CHANGING THE MAC ADDRESS

##############################

def tui_cd_change_mac_address(mac_changer_script_file_path):
    allow_connecting_back_to_wifi = ask_confirmation(
        "Do you want to connect back to the internet? (y/n): "
    )
    change_mac_address(
        mac_changer_script_file_path=mac_changer_script_file_path,
        is_positive=allow_connecting_back_to_wifi,
        is_using_gui=is_using_gui
    )

##############################

# CHANGING THE NAMESERVERS

##############################

def tui_cd_change_dns(
    nameserver_changer_file_path,
    tor_nameservers_file_path,
    original_resolv_configuration_file_path,
    privacy_focused_nameservers_file_path,
    ghostsurf_settings_file_path
):
    config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
    if config["is_ghostsurf_on"] == "True":
        is_working = True
    else:
        is_working = False
    change_nameservers(
        is_working=is_working,
        nameserver_changer_file_path=nameserver_changer_file_path,
        tor_nameservers_file_path=tor_nameservers_file_path,
        original_resolv_configuration_file_path=original_resolv_configuration_file_path,
        privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path,
        is_using_gui=is_using_gui,
    )

##############################

# CHANGING THE HOSTNAME

##############################

def tui_cd_change_hostname(hostname_changer_script_file_path):
    allow_reboot = ask_confirmation(
        "This operation requires reboot. Do you allow to reboot this system? (y/n): "
    )
    if allow_reboot:
        change_hostname(
            hostname_changer_script_file_path=hostname_changer_script_file_path,
            is_using_gui=is_using_gui,
        )
    else:
        message = "Operationg cancelled."
        display_notification(
            is_using_gui=is_using_gui,
            message=message,
        )

##############################

# DISPLAYING THE HELP PAGE

##############################

def tui_cd_display_the_help_page(url):
    wbopen(url)
    print("Help page has been opened in your default browser.")

##############################

# WIPING MEMORY

##############################

def tui_cd_wipe_memory(fast_bomb_script_file_path, secure_bomb_script_file_path):
    allow_less_secure_memory_wipe = ask_confirmation(
        "Do you want fast and less secure operation? (y/n): "
    )

    if allow_less_secure_memory_wipe:
        wipe_memory_less_securely(
            fast_bomb_script_file_path=fast_bomb_script_file_path,
            is_using_gui=is_using_gui,
        )
    else:
        wipe_memory_high_securely(
            secure_bomb_script_file_path=secure_bomb_script_file_path,
            is_using_gui=is_using_gui,
        )

##############################

# SHREDING LOGS

##############################

def tui_cd_shred_logs(log_shredder_file_path, current_username):
    shred_log_files(
        log_shredder_file_path=log_shredder_file_path,
        current_username=current_username,
        is_using_gui=is_using_gui,
    )

##############################

# ANONYMIZING THE BROWSER

##############################

def tui_cd_anonymize_browser(
    firefox_profiles_dir,
    custom_firefox_preferences_file_path,
    init_script_file_path,
    firefox_profiles_conf_file_path
):
    anonymize_browser(
        init_script_file_path=init_script_file_path,
        firefox_profiles_dir=firefox_profiles_dir,
        custom_firefox_preferences_file_path=custom_firefox_preferences_file_path,
        firefox_profiles_conf_file_path=firefox_profiles_conf_file_path,
        is_using_gui=is_using_gui,
    )

##############################

# RESETING

##############################

def tui_cd_reset(reset_script_file_path):
    allow_resetting_iptables_rules_only = ask_confirmation(
        "Are you sure you want to revert all changes and restore the defaults? (y/n): "
    )
    if allow_resetting_iptables_rules_only:
        reset_changes(
            reset_script_file_path=reset_script_file_path,
            is_using_gui=is_using_gui,
        )

##############################

# PERFORM CHECKS

##############################

def tui_cd_checklist(
    fake_hostnames_list_file_path,
    privacy_focused_nameservers_file_path,
    original_resolv_configuration_file_path,
    current_username,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path,
    timezone_backup_file_path,
    ghostsurf_settings_file_path
):
    checklist_items_dict = {
        'Using fake hostname': False,
        'Using fake mac address': False,
        'Using appropriate nameservers': False,
        'Ghostsurf\'s Firefox profiles are available. And, preferences are set': False,
        'Using different timezone': False,
        'Using a tor connection': False,
    }
    check_fake_hostname_usage(
        fake_hostnames_list_file_path=fake_hostnames_list_file_path,
        checklist_items_dict=checklist_items_dict
    )
    check_fake_mac_address_usage(checklist_items_dict=checklist_items_dict)
    check_appropriate_nameserver_usage(
        privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path,
        original_resolv_configuration_file_path=original_resolv_configuration_file_path,
        checklist_items_dict=checklist_items_dict,
        ghostsurf_settings_file_path=ghostsurf_settings_file_path
    )
    check_browser_anonymization(
        current_username=current_username,
        checklist_items_dict=checklist_items_dict,
        firefox_profiles_dir=firefox_profiles_dir,
        custom_firefox_preferences_file_path=custom_firefox_preferences_file_path
    )
    check_different_timezone_usage(
        timezone_backup_file_path=timezone_backup_file_path,
        checklist_items_dict=checklist_items_dict
    )
    check_tor_connection_usage(checklist_items_dict=checklist_items_dict)
    print("Anonymity Checklist")
    for k, v in checklist_items_dict.items():
        print(f"{k} = {v}")