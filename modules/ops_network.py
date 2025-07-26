# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from requests import get as requestsget
from requests.exceptions import RequestException, Timeout
from re import compile as recompile
from subprocess import run, check_call, CalledProcessError, TimeoutExpired

# Ghostsurf Modules
from modules.conf_logging import debug, info, error
from modules.conf_notification import display_notification
from modules.conf_ghostsurf import load_ghostsurf_config

##############################

# GET PUBLIC IP ADDRESS

##############################

def get_public_ip_address(is_using_gui=False, ghostsurf_logo_file_path=None, timeout_seconds=7.5):
    url = "https://ifconfig.io"
    try:
        response = requestsget(url, timeout=timeout_seconds, headers={"User-Agent": "curl"})
        response.raise_for_status()

        ip = response.text.strip()

        ipv4_pattern = recompile(r'^\d{1,3}(\.\d{1,3}){3}$')
        ipv6_pattern = recompile(r'^([a-fA-F0-9:]+:+)+[a-fA-F0-9]+$')

        if ipv4_pattern.fullmatch(ip) or ipv6_pattern.fullmatch(ip):
            message = f'Your public IP address is {ip}.'
            info(f"Retrieved IP: {ip}")
        else:
            message = "Couldn't verify the IP address format!"
            error(f"Unexpected IP response format: {ip}")

        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message
        )
        info("Public IP address retrieved successfully.")

    except Timeout:
        message = "Timeout while retrieving public IP address."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except RequestException as e:
        message = "Network error occurred while retrieving public IP."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error while getting public IP."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# CHANGE PUBLIC IP ADDRESS

##############################

def change_public_ip_address(is_using_gui=False, ghostsurf_logo_file_path=None):
    try:
        if is_using_gui:
            check_call(["pkexec", "systemctl", "restart", "tor"])
        else:
            check_call(["sudo", "systemctl", "restart", "tor"])
        message = "Tor service has been restarted to change your public IP address."
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message
        )
        info("Tor service has been restarted.")
    except CalledProcessError as e:
        message = "Failed to restart Tor service. Is pkexec working correctly?"
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message
        )
    except Exception as e:
        message = "Unexpected error occurred while restarting Tor."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message
        )

##############################

# CHANGE MAC ADDRESS

##############################

def change_mac_address(
    mac_changer_script_file_path,
    is_positive=False,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    if is_positive:
        try:
            # Identify the active internet interface (e.g., wlan0)
            result = run(
                "ip route show default | awk '/default/ {print $5}'",
                shell=True, capture_output=True, text=True, check=True
            )
            interface_name = result.stdout.strip()
            if not interface_name:
                error("Failed to detect network interface. Aborting MAC address change.")
                return

            debug(f"Detected interface for reconnection: {interface_name}")
            # Construct and execute the combined command securely
            command = f"bash {mac_changer_script_file_path} && sleep 4 && nmcli d connect {interface_name}"
            check_call(["pkexec", "bash", "-c", command])
            message = "MAC address has been changed and the device has reconnected to the internet."
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
            info("MAC address has been changed.")
        except CalledProcessError as e:
            message = "MAC changer subprocess failed."
            error(f"{message} - {e}")
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
        except Exception as e:
            message = "Unexpected error occurred while changing the mac address."
            error(f"{message} - {e}")
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
    else:
        try:
            check_call(["pkexec", "bash", mac_changer_script_file_path])
            message = "MAC address has been changed."
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
            info("MAC address has been changed.")
        except CalledProcessError as e:
            message = "MAC changer subprocess failed."
            error(f"{message} - {e}")
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
        except Exception as e:
            message = "Unexpected error occurred while changing MAC address."
            error(f"{message} - {e}")
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )

##############################

# CHANGE NAMESERVERS

##############################

def change_nameservers(
    is_working,
    nameserver_changer_file_path,
    tor_nameservers_file_path,
    original_resolv_configuration_file_path,
    privacy_focused_nameservers_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        if is_working == True:
            command_string = (
                f"{nameserver_changer_file_path} {tor_nameservers_file_path} && "
                f"cp {tor_nameservers_file_path} {original_resolv_configuration_file_path}"
            )
        else:
            command_string = (
                f"{nameserver_changer_file_path} {privacy_focused_nameservers_file_path} && "
                f"cp {privacy_focused_nameservers_file_path} {original_resolv_configuration_file_path}"
            )
        check_call(["pkexec", "bash", "-c", command_string])
        message = "Nameservers have been changed."
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        info("Nameservers have been changed.")
    except CalledProcessError as e:
        message = "Nameserver changer subprocess failed."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
    except Exception as e:
        message = "Unexpected error occurred while changing nameservers."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)

##############################

# GET TOR STATUS

##############################

def get_tor_status(
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    is_tor_service_active = False
    try:
        output = run(
            ["systemctl", "is-active", "tor"],
            text=True,
            capture_output=True,
            timeout=5,
            check=False # Avoid raising on non-zero exit
        ).stdout.strip().lower()

        if is_using_gui == False:
            if output == "active":
                is_tor_service_active = True
            else:
                is_tor_service_active = False
            message = f"Is Tor service active: {is_tor_service_active}."
            display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        else:
            if output == "active":
                return 'active'
            elif output == "inactive":
                return 'inactive'
            else:
                return 'unknown'
        info("Tor status has been retreived.")
    except TimeoutExpired:
        message = "Timed out while checking Tor service status."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        if is_using_gui:
            return 'unknown'
    except Exception as e:
        message = "Unexpected error occurred while getting tor status."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        if is_using_gui:
            return 'unknown'

##############################

# UPDATE TOR STATUS

##############################

def update_tor_status_label(
    label_widget,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        status = get_tor_status(
            is_using_gui=is_using_gui,
        )
        style_map = {
            'inactive': ('color: red;', 'Inactive'),
            'active':   ('color: green;', 'Active'),
            'unknown':  ('color: gray;', 'Unknown')
        }
        style, text = style_map.get(status, ('color: gray;', 'Unknown'))
        label_widget.setStyleSheet(f"#status_label {{ {style} }}")
        label_widget.setText(text)
        message = message = "Tor status label have been updated."
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
    except Exception as e:
        message = message = "Unexpected error occurred while updating tor status label."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)

##############################

# GET PROXY STATUS

##############################

def get_proxy_status(
    ghostsurf_settings_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    is_transparent_proxy_on = False
    try:
        config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
        if config["is_ghostsurf_on"] == "True":
            is_transparent_proxy_on = True
        else:
            is_transparent_proxy_on = False
        message = f"Is transparent proxy turned on: {is_transparent_proxy_on}"
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        info("Proxy status has been retreived.")
    except Exception as e:
        message = message = "Unexpected error occurred while getting tor status."
        error(f"{message} - {e}")
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)