# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from sys import exit as sysexit
from os import geteuid
from pathlib import Path

# Ghostsurf Modules
from modules.conf_logging import debug, error

##############################

# CHECK PRIVILEGES

##############################

def check_root_privileges():
    try:
        effective_user_id = geteuid()
        debug(f"Effective User ID: {effective_user_id}")

        if effective_user_id == 0:
            message = "Running as root is not allowed."
            print(message)
            sysexit()

    except Exception as e:
        error(f"Failed to check root privileges: {e}")
        sysexit()

##############################

# VALIDATE PATHS

##############################

def validate_ghostsurf_paths(paths_dict):
    try:
        missing_paths = []

        for label, path in paths_dict.items():
            if isinstance(path, str):
                resolved_path = Path(path)
            else:
                resolved_path = path

            if not resolved_path.is_file():
                error(f"Missing required file: {label} at {resolved_path}")
                missing_paths.append(f"{label}: {resolved_path}")

        if missing_paths:
            message = "Missing required files:\n" + "\n".join(missing_paths)
            print(message)
            sysexit()

    except Exception as e:
        error(f"Failed to validate files.")
        sysexit()