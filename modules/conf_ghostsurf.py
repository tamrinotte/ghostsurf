# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from json import load, dump

# Ghostsurf Modules
from modules.conf_logging import error

##############################

# LOAD GHOSTSURF CONFIG

##############################

def load_ghostsurf_config(ghostsurf_settings_file_path):
    with open(ghostsurf_settings_file_path, 'r') as file:
        return load(file)

##############################

# SAVE GHOSTSURF CONFIG

##############################

def save_ghostsurf_config(ghostsurf_settings_file_path, config):
    with open(ghostsurf_settings_file_path, 'w') as file:
        dump(config, file, indent=4)

##############################

# UPDATE GHOSTSURF STATUS

##############################

def update_ghostsurf_status(config_path, status):
    try:
        config = load_ghostsurf_config(config_path)
        config["is_ghostsurf_on"] = str(status)
        save_ghostsurf_config(config_path, config)
    except Exception as e:
        error(f"Failed to update Ghostsurf config: {e}")
