# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from subprocess import run
from json import load, dump

# Ghostsurf Modules
from modules.logging_config import (
    debug,
    info,
    warning,
    error,
)

##############################

# STANDARD FUNCTIONS

##############################

def load_ghostsurf_config(ghostsurf_settings_file_path):
    with open(ghostsurf_settings_file_path, 'r') as file:
        return load(file)

def save_ghostsurf_config(ghostsurf_settings_file_path, config):
    with open(ghostsurf_settings_file_path, 'w') as file:
        dump(config, file, indent=4)