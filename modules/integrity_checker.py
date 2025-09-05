# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import sys
import os
import pathlib

# Ghostsurf Modules
from modules.conf_logging import debug, error

##############################

# CHECK PRIVILEGES

##############################

def check_root_privileges():
    try:
        effective_user_id = os.geteuid()
        debug(f"Effective User ID: {effective_user_id}")

        if effective_user_id == 0:
            message = "Running as root is not allowed."
            print(message)
            sys.exit()

    except Exception as e:
        error(f"Failed to check root privileges: {e}")
        sys.exit()

##############################

# VALIDATE PATHS

##############################

def validate_ghostsurf_paths(paths_dict):
    try:
        missing_paths = []

        for label, path in paths_dict.items():
            if isinstance(path, str):
                resolved_path = pathlib.Path(path)
            else:
                resolved_path = path

            if not resolved_path.is_file():
                error(f"Missing required file: {label} at {resolved_path}")
                missing_paths.append(f"{label}: {resolved_path}")

        if missing_paths:
            message = "Missing required files:\n" + "\n".join(missing_paths)
            print(message)
            sys.exit()

    except Exception as e:
        error(f"Failed to validate files.")
        sys.exit()