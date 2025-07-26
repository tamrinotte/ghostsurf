# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from subprocess import run, check_call, CalledProcessError
from re import compile as recompile
from pathlib import Path

# Ghostsurf Modules
from modules.conf_logging import debug, info, error
from modules.conf_notification import display_notification

##############################

# CHANGE HOSTNAME

##############################

def change_hostname(
    hostname_changer_script_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        check_call(["pkexec", "bash", "-c", f"bash '{hostname_changer_script_file_path}' && reboot"])
    except CalledProcessError as e:
        message = "Hostname changer subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while changing system's hostname."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# WIPE MEMORY

##############################

def wipe_memory(
    is_positive,
    fast_bomb_script_file_path,
    secure_bomb_script_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    script = fast_bomb_script_file_path if is_positive else secure_bomb_script_file_path
    message = "Memory wipe completed successfully."
    
    try:
        result = run(["pkexec", "bash", script])
        if result.returncode == 0:
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
            info(message)
        else:
            message = "Memory wipe was interrupted or partially completed."
            warning(message)
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message=message,
            )
    except Exception as e:
        message = "Unexpected error occurred while wiping the memory."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# SECURE DELETE LOG FILES

##############################

def shred_log_files(
    log_shredder_file_path,
    current_username,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        check_call(["pkexec", "bash", log_shredder_file_path, current_username])
        message = "Log files have been shredded."
        display_notification(is_using_gui=is_using_gui, icon_file_path=ghostsurf_logo_file_path, message=message)
        info("Log files have been shredded.")
    except CalledProcessError as e:
        message = "Log shredder subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while securely deleting log files."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )

##############################

# ANONYMIZE BROWSER

##############################

def anonymize_browser(
    init_script_file_path,
    firefox_profiles_dir,
    custom_firefox_preferences_file_path,
    firefox_profiles_conf_file_path,
    is_using_gui=False,
    ghostsurf_logo_file_path=None,
):
    try:
        check_call(["pkexec", "bash", init_script_file_path])
        ghostsurf_pattern = recompile(r".*ghostsurf$")
        pentest_pattern = recompile(r".*penetration-testing$")
        ghostsurf_dir = None
        pentest_dir = None

        for profile_path in firefox_profiles_dir.iterdir():
            if profile_path.is_dir():
                if ghostsurf_pattern.match(profile_path.name):
                    ghostsurf_dir = profile_path
                    debug(f"Found Ghostsurf profile: {ghostsurf_dir}")
                elif pentest_pattern.match(profile_path.name):
                    pentest_dir = profile_path
                    debug(f"Found Penetration-Testing profile: {pentest_dir}")

        # --- Handle Ghostsurf profile creation ---
        if not ghostsurf_dir:
            check_call(["firefox-esr", "-CreateProfile", "ghostsurf"])

            # Find new profile directory
            ghostsurf_dirs = list(firefox_profiles_dir.glob("*.ghostsurf"))
            if not ghostsurf_dirs:
                raise Exception("Failed to create Ghostsurf Firefox profile.")
            ghostsurf_dir = ghostsurf_dirs[0]

            # Load custom preferences
            if not custom_firefox_preferences_file_path.exists():
                return

            with open(custom_firefox_preferences_file_path, "r") as f:
                custom_prefs = f.read().strip()

            user_js_path = Path(ghostsurf_dir, "user.js")
            debug(f"Writing preferences to {user_js_path}")
            with open(user_js_path, "w") as f:
                f.write(custom_prefs)

            # Update Firefox profile configuration
            if not firefox_profiles_conf_file_path.exists():
                raise Exception(f"Firefox profiles config file not found: {firefox_profiles_conf_file_path}")

            with open(firefox_profiles_conf_file_path, "r") as f:
                conf_lines = f.readlines()

            ghostsurf_profile_path_spec = None
            default_index = None

            for idx, line in enumerate(conf_lines):
                if "Path=" in line and "ghostsurf" in line:
                    ghostsurf_profile_path_spec = line.split("=")[1].strip()
                if line.startswith("Default="):
                    default_index = idx

            if ghostsurf_profile_path_spec and default_index is not None:
                conf_lines[default_index] = f"Default={ghostsurf_profile_path_spec}\n"
                with open(firefox_profiles_conf_file_path, "w") as f:
                    f.writelines(conf_lines)
                debug(f"Updated default profile to Ghostsurf: {ghostsurf_profile_path_spec}")

            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message="Ghostsurf Firefox profile has been created and configured."
            )

        # --- Handle Penetration-Testing profile creation ---
        if not pentest_dir:
            check_call(["firefox-esr", "-CreateProfile", "penetration-testing"])
            display_notification(
                is_using_gui=is_using_gui,
                icon_file_path=ghostsurf_logo_file_path,
                message="Penetration-Testing Firefox profile has been created."
            )

    except CalledProcessError as e:
        message = "Browser anonymizer subprocess failed."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )
    except Exception as e:
        message = "Unexpected error occurred while anonymizing browser."
        error(f"{message} - {e}")
        display_notification(
            is_using_gui=is_using_gui,
            icon_file_path=ghostsurf_logo_file_path,
            message=message,
        )