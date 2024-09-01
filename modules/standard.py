# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from subprocess import run
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from json import load, dump

# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)



##############################

# STANDARD FUNCTIONS

##############################

def load_ghostsurf_config(ghostsurf_settings_file_path):
    """A function which loads configurations from settings json file."""

    with open(ghostsurf_settings_file_path, 'r') as file:
        return load(file)

def save_ghostsurf_config(ghostsurf_settings_file_path, config):
    """A function which saves configs into settings json file."""

    with open(ghostsurf_settings_file_path, 'w') as file:
        dump(config, file, indent=4)

def manage_netfilter_service(user_pwd):
    """A function which starts and enables netfilter service if it's not"""

    netfilter_persistent_status = run(["sudo", "-S", "systemctl", "status", "netfilter-persistent"], input=user_pwd, capture_output=True, text=True).stdout.strip()

    if 'inactive' in netfilter_persistent_status:

        run(["sudo", "-S", "systemctl", "start", "netfilter-persistent"], text=True, input=user_pwd)
        debug("Starting netfilter-persistent.service")

    if 'disabled' in netfilter_persistent_status:

        run(["sudo", "-S", "systemctl", "enable", "netfilter-persistent"], text=True, input=user_pwd)
        debug("Enabling netfilter-persistent.service")
