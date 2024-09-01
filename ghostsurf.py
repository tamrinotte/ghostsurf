# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from pathlib import Path
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from webbrowser import open as wbopen
from time import sleep
from getpass import getuser
from sys import argv, exit as sysexit
from subprocess import run
from threading import Thread
from re import compile
from json import load, dump
import argparse

# PySide6
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QMessageBox,
    QLineEdit,
)
from PySide6.QtGui import QImage
from PySide6.QtCore import (
    QAbstractListModel,
    Qt,
    QRunnable,
    QThreadPool,
    QThread,
    QObject,
    Signal,
    Slot,
)

# GUIs
from ui.main_win_ui import Ui_MainWindow
from ui.password_win_ui import Ui_PasswordWindow
from ui.checklist_win_ui import Ui_ChecklistWindow

# Resources
import resources_rc

# Ghostsurf Modules
from modules.check_list import (
    check_fake_hostname_usage, 
    check_fake_mac_address_usage, 
    check_appropriate_nameserver_usage, 
    check_browser_anonymization,
    check_different_timezone_usage,
    check_tor_connection_usage,
)

from modules.control_deck import (
    cd_show_ip,
    cd_shred_logs,
    cd_reset,
    cd_change_mac_address,
    cd_wipe_memory,
    cd_change_nameservers,
    cd_anonymize_browser,
    cd_change_hostname,
)

from modules.standard import (
    load_ghostsurf_config,
    save_ghostsurf_config,
    manage_netfilter_service,
)

from modules.text_based_ui import (
    tui_start_transparent_proxy,
    tui_stop_transparent_proxy,
    tui_change_ip,
    tui_show_ip,
    tui_show_status,
    tui_change_mac_address,
    tui_change_dns,
    tui_change_hostname,
    tui_display_the_help_page,
    tui_anonymize_browser,
    tui_wipe_memory,
    tui_shred_logs,
    tui_checklist,
    tui_reset,
    tui_enable_at_boot,
    tui_disable_at_boot,
)

# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)



##############################

# GLOBAL VARIABLES

##############################

current_username = getuser()
help_page_url = "https://www.github.com/tamrinotte/ghostsurf#readme"
base_dir = Path(__file__).parent

# CONFIGURATION FILE PATHS

configuration_files_dir_path = Path(base_dir, "configuration_files")
ghostsurf_settings_file_path = Path(configuration_files_dir_path, "ghostsurf_settings.json")
privacy_focused_nameservers_file_path = Path(configuration_files_dir_path, "privacy_focused_nameservers_resolv.conf")
tor_nameservers_file_path = Path(configuration_files_dir_path, "tor_nameservers_resolv.conf")
original_resolv_configuration_file_path = Path("/etc/resolv.conf")
fake_hostnames_list_file_path = Path(configuration_files_dir_path, "list_of_fake_hostnames.list")
firefox_profiles_dir = Path(f"/home/{current_username}/.mozilla/firefox/")
firefox_profiles_conf_file_path = Path(firefox_profiles_dir, "profiles.ini")
custom_firefox_preferences_file_path = Path(configuration_files_dir_path, "firefox_prefs.js.custom")

# ICON FILE PATH

icons_dir_path = Path(base_dir, "icons")
ghostsurf_logo_file_path = Path(icons_dir_path, "ghostsurf.png")

# BASH SCRIPT FILE PATHS

bash_scripts_dir_path = Path(base_dir, "bash_scripts")
mac_changer_script_file_path = Path(bash_scripts_dir_path, "mac_changer.sh")
fast_bomb_script_file_path = Path(bash_scripts_dir_path, "fast_bomb.sh")
secure_bomb_script_file_path = Path(bash_scripts_dir_path, "secure_bomb.sh")
reset_script_file_path = Path(bash_scripts_dir_path, "reset.sh")
reset_iptables_only_script_file_path = Path(bash_scripts_dir_path, "reset_iptables_only.sh")
start_transparent_proxy_script_file_path = Path(bash_scripts_dir_path, "start_transparent_proxy.sh")
stop_transparent_proxy_script_file_path = Path(bash_scripts_dir_path, "stop_transparent_proxy.sh")
hostname_changer_script_file_path = Path(bash_scripts_dir_path, "hostname_changer.sh")
save_iptables_script_file_path = Path(bash_scripts_dir_path, "save_iptables_rules.sh")
init_script_file_path = Path(bash_scripts_dir_path, "init.sh")
log_shredder_file_path = Path(bash_scripts_dir_path, "log_shredder.sh")
nameserver_changer_file_path = Path(bash_scripts_dir_path, "nameservers_changer.sh")

# BACKUP FILE PATH

timezone_backup_file_path = Path("/opt/ghostsurf/backup_files/timezone.backup")

# ICONS

tick = QImage(str(Path(icons_dir_path, "tick.png")))
cross = QImage(str(Path(icons_dir_path, "cross.png")))



##############################

# THE MAIN FUNCTION

##############################

def main():
    """The function which runs the entire application"""

    if current_username == "root":

        run(["notify-send", "-i", ghostsurf_logo_file_path, "-t", "150", "You can't run this app as the root user."], text=True)
        sysexit()

    else:

        if len(argv) == 1:
        
            app = QApplication([])
            password_window = PasswordWindow()
            password_window.show()
            sysexit(app.exec())

        else:

            parser = argparse.ArgumentParser(description='GhostSurf CLI')
            subparsers = parser.add_subparsers(dest='command')

            start_parser = subparsers.add_parser('start', help='Start transparent proxy')
            start_parser.set_defaults(func=lambda: tui_start_transparent_proxy(init_script_file_path, start_transparent_proxy_script_file_path, ghostsurf_settings_file_path))

            stop_parser = subparsers.add_parser('stop', help='Stop transparent proxy')
            stop_parser.set_defaults(func=lambda: tui_stop_transparent_proxy(init_script_file_path, stop_transparent_proxy_script_file_path, ghostsurf_settings_file_path))

            change_ip_parser = subparsers.add_parser('changeip', help="Change my IP")
            change_ip_parser.set_defaults(func=tui_change_ip)

            my_ip_parser = subparsers.add_parser('myip', help="Show my public IP address")
            my_ip_parser.set_defaults(func=tui_show_ip)

            status_parser = subparsers.add_parser('status', help="Show if transparent proxy is on/off")
            status_parser.set_defaults(func=lambda: tui_show_status(ghostsurf_settings_file_path))

            change_mac_parser = subparsers.add_parser('changemac', help="Change my mac address")
            change_mac_parser.set_defaults(func=lambda: tui_change_mac_address(mac_changer_script_file_path))

            change_dns_parser = subparsers.add_parser('changedns', help="Change my DNS")
            change_dns_parser.set_defaults(func=lambda: tui_change_dns(nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path, ghostsurf_settings_file_path))

            change_hostname = subparsers.add_parser('changehostname', help="Change my hostname")
            change_hostname.set_defaults(func=lambda: tui_change_hostname(stop_transparent_proxy_script_file_path, hostname_changer_script_file_path))
            
            white_rabbit_parser = subparsers.add_parser('whiterabbit', help="Follow the white rabbit")
            white_rabbit_parser.set_defaults(func=lambda: tui_display_the_help_page(help_page_url))

            pandora_bomb_parser = subparsers.add_parser('pandorabomb', help="Wipe the RAM")
            pandora_bomb_parser.set_defaults(func=lambda: tui_wipe_memory(fast_bomb_script_file_path, secure_bomb_script_file_path))

            browser_anonymization_parser = subparsers.add_parser('anonymizebrowser', help="Anonymize firefox")
            browser_anonymization_parser.set_defaults(func=lambda: tui_anonymize_browser(firefox_profiles_dir, custom_firefox_preferences_file_path, init_script_file_path, firefox_profiles_conf_file_path))

            log_shedder_parser = subparsers.add_parser('shredlogs', help="Shred log files")
            log_shedder_parser.set_defaults(func=lambda: tui_shred_logs(log_shredder_file_path, current_username))

            checklist_parser = subparsers.add_parser('checklist', help="Run anonymity checklist")
            checklist_parser.set_defaults(func=lambda: tui_checklist(fake_hostnames_list_file_path, privacy_focused_nameservers_file_path, original_resolv_configuration_file_path, current_username, firefox_profiles_dir, custom_firefox_preferences_file_path, timezone_backup_file_path, ghostsurf_settings_file_path))

            reset_parser = subparsers.add_parser('reset', help="Reset changes")
            reset_parser.set_defaults(func=lambda: tui_reset(reset_iptables_only_script_file_path, reset_script_file_path))

            enabled_parser = subparsers.add_parser('enable', help="Enable Ghostsurf at boot")
            enabled_parser.set_defaults(func=lambda: tui_enable_at_boot(start_transparent_proxy_script_file_path, save_iptables_script_file_path, ghostsurf_settings_file_path))

            disabled_parser = subparsers.add_parser('disable', help="Disable Ghostsurf at boot")
            disabled_parser.set_defaults(func=lambda: tui_disable_at_boot(stop_transparent_proxy_script_file_path, save_iptables_script_file_path, ghostsurf_settings_file_path))

            args = parser.parse_args()

            if hasattr(args, 'func'):

                args.func()

            else:

                parser.print_help()



##############################

# WORKERS

##############################

class CheckListWorkerSignals(QObject):
    """A worker signals class which defines the signals available from a running worker thread."""

    list_item = Signal(str)

class CheckListWorker(QRunnable):
    """A worker class which inherits from QRunnable to handle worker thread setup, signals and wrap-up."""

    def __init__(self):
        """An init function to initialize class's objects."""

        super().__init__()
        self.signals = CheckListWorkerSignals()

    global checklist_items_dict
    checklist_items_dict = {
        'Using fake hostname': False,
        'Using fake mac address': False,
        'Using appropriate nameservers': False,
        'Ghostsurf\'s Firefox profiles are available. And, preferences are set': False,
        'Using different timezone': False,
        'Using a tor connection': False,
        'Using man in the middle protection': False
    }

    @Slot()
    def run(self):
        """A function which runs all checklist functions and updates the checklist dictionary."""

        check_fake_hostname_usage(fake_hostnames_list_file_path=fake_hostnames_list_file_path, checklist_items_dict=checklist_items_dict)
        check_fake_mac_address_usage(checklist_items_dict=checklist_items_dict)
        check_appropriate_nameserver_usage(privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path, original_resolv_configuration_file_path=original_resolv_configuration_file_path, checklist_items_dict=checklist_items_dict, ghostsurf_settings_file_path=ghostsurf_settings_file_path)
        check_browser_anonymization(current_username=current_username, checklist_items_dict=checklist_items_dict, firefox_profiles_dir=firefox_profiles_dir, custom_firefox_preferences_file_path=custom_firefox_preferences_file_path)
        check_different_timezone_usage(timezone_backup_file_path=timezone_backup_file_path, checklist_items_dict=checklist_items_dict)
        check_tor_connection_usage(checklist_items_dict=checklist_items_dict)

        for key in checklist_items_dict.keys():

            self.signals.list_item.emit(key)
            sleep(0.02)



##############################

# DATA MODELS

##############################

class ChecklistModel(QAbstractListModel):
    """A data class called ChacklistModel designed to manage the creation of data objects."""

    def __init__(self, list_items=None): # list_items=None is a default value
        """An init function to initialize class's objects."""

        super().__init__()
        self.list_items = list_items or []

    def data(self, index, role):
        """A function returns data for the given index and role, handling display and decoration roles."""

        if role == Qt.DisplayRole:

            status, text = self.list_items[index.row()]
            return text

        if role == Qt.DecorationRole:

            status, text = self.list_items[index.row()]
            
            if status:

                return tick

            else:

                return cross

    def rowCount(self, index):
        """A function wihch returns the row count from the data table."""

        return len(self.list_items)



##############################

# CHECK LIST WINDOW

##############################

class ChecklistWindow(QWidget, Ui_ChecklistWindow):
    """A class representing the checklist window's graphical user interface, built as a QWidget and utilizes a user interface called Ui_ChecklistWindow."""

    def __init__(self, *args, **kwargs):
        """An init function initializes the window, setting up the user interface and it's internal state for window to function.""" 

        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = ChecklistModel()
        self.threadpool = QThreadPool()
        self.checklist_list_view.setModel(self.model)
        worker = CheckListWorker()
        worker.signals.list_item.connect(self.run_all_the_checks)
        self.threadpool.start(worker)

    def run_all_the_checks(self, key):
        """A function which calls all of the checking functions and adds the checklist items to the checklist"""

        self.model.list_items.append((checklist_items_dict[key], key))
        self.model.layoutChanged.emit()



##############################

# PASSWORD WINDOW

##############################

class PasswordWindow(QWidget, Ui_PasswordWindow):
    """A window class representing the password window interface, built as a QWidget and utilizes a user interface called Ui_PasswordWindow"""

    def __init__(self, *args, **kwargs):
        """An init function initializes the window, setting up the user interface and it's internal state for window to function.""" 

        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.submit_button.pressed.connect(self.get_user_pwd)
        self.visibility_button.pressed.connect(self.change_echo_mode)

    def change_echo_mode(self):
        """A function which changes the echo mode to hide or display the password in the input area."""

        echo_mode = self.password_line_edit.echoMode()

        if echo_mode == QLineEdit.EchoMode.Password:

            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)

        else:

            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def get_user_pwd(self):
        """A function which stores the password that the user entered in a global variable"""

        global user_pwd
        user_pwd = str(self.password_line_edit.text())
        user_name = run(["sudo", "-S", "whoami"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if user_name == "root":

            self.close()
            global main_window
            main_window = MainWindow()
            main_window.show()

        else:

            warning_dialog = QMessageBox()
            warning_dialog.setIcon(QMessageBox.Critical)
            warning_dialog.setWindowTitle("Warning")
            warning_dialog.setText("Couldn't get root privileges!")
            warning_dialog.exec()



##############################

# MAIN WINDOW

##############################

class MainWindow(QMainWindow, Ui_MainWindow):
    """A window class representing the main window interface, built as a QMainWindow with a user interface from Ui_MainWindow."""

    def __init__(self, *args, **kwargs):
        """An init function initializes the window, setting up te user interface and internal state for window to function.""" 

        super().__init__(*args, **kwargs)
        self.setupUi(self)
        manage_netfilter_service(user_pwd=user_pwd)
        ghostsurf_config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)

        if ghostsurf_config["is_enabled_at_boot"] == "True": 
            self.start_stop_button.setText("Stop")
            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')
            self.ultra_ghost_button.setText("enabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")
        
        tor_status = run(["sudo", "-S", "systemctl", "status", "tor"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

        self.start_stop_button.pressed.connect(self.start_stop)
        self.my_ip_button.pressed.connect(self.show_ip)
        self.status_button.pressed.connect(self.show_status)
        self.change_ip_button.pressed.connect(self.change_ip)
        self.info_button.pressed.connect(self.display_the_help_page)
        self.run_fast_check_button.pressed.connect(self.run_checklist)
        self.dns_changer_button.pressed.connect(self.change_nameservers)
        self.browser_anonymizer_button.pressed.connect(self.anonymize_browser)
        self.hostname_changer_button.pressed.connect(self.change_hostname)
        self.mac_changer_button.pressed.connect(self.change_mac_address)
        self.ultra_ghost_button.pressed.connect(self.ultra_ghost_mode)
        self.log_shredder_button.pressed.connect(self.shred_log_files)
        self.pandora_bomb_button.pressed.connect(self.wipe_memory)
        self.reset_button.pressed.connect(self.reset_settings)

    def start_stop(self):
        """A function which redirects all internet traffic over tor."""

        def start_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the start button is pressed to identify what app should do."""

            user_answer = i.text()

            if user_answer == "&Yes":

                debug("Yes button is clicked")
                run(["sudo", "-S", init_script_file_path], text=True, input=user_pwd)
                run(["sudo", "-S", start_transparent_proxy_script_file_path], text=True, input=user_pwd)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "True"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Stop")

            elif user_answer == "&No":

                debug("No button is clicked")
                run(["sudo", "-S", start_transparent_proxy_script_file_path], text=True, input=user_pwd)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "True"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Stop")

            else:

                debug("Operation canceled")

        def stop_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the stop button is pressed to identify what app should do."""

            user_answer = i.text()

            if user_answer == "&Yes":

                run(["sudo", "-S", init_script_file_path], text=True, input=user_pwd)
                run(["sudo", "-S", stop_transparent_proxy_script_file_path], text=True, input=user_pwd)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_enabled_at_boot"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Start")
                self.ultra_ghost_button.setText("disabled")
                self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")

            elif user_answer == "&No":

                run(["sudo", "-S", stop_transparent_proxy_script_file_path], text=True, input=user_pwd)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_enabled_at_boot"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)

                self.start_stop_button.setText("Start")
                self.ultra_ghost_button.setText("disabled")
                self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")

            else:

                debug("Operation canceled")

        if self.start_stop_button.text() == "Start":

            debug("Start button pressed")
            question_dialog = QMessageBox()
            question_dialog.setIcon(QMessageBox.Question)
            question_dialog.setWindowTitle("Important")
            question_dialog.setText("Are you allowing to killing of dangerous applications and cleaning of dangerous caches?")
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            question_dialog.buttonClicked.connect(start_button_question_dialog_processor)
            question_dialog.exec()

        else:

            debug("Stop button pressed")
            question_dialog = QMessageBox()
            question_dialog.setIcon(QMessageBox.Question)
            question_dialog.setWindowTitle("Important")
            question_dialog.setText("Are you allowing to killing of dangerous applications and cleaning of dangerous caches?")
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            question_dialog.buttonClicked.connect(stop_button_question_dialog_processor)
            question_dialog.exec() 

        tor_status = run(["sudo", "-S", "systemctl", "status", "tor"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def show_ip(self):
        """A function which shows your public ip address."""

        public_ip_thread = Thread(target=cd_show_ip, args=[user_pwd, ghostsurf_logo_file_path])
        public_ip_thread.start()

    def show_status(self):
        """A function which shows the tor service's status."""

        tor_status = run(["sudo", "-S", "systemctl", "status", "tor"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def change_ip(self):
        """A function which changes your ip address by restarting the transparent proxy."""

        debug("Change IP button has been clicked!")
        run(["sudo", "-S", "systemctl", "restart", "tor"], text=True, input=user_pwd)

    def display_the_help_page(self):
        """A function which opens the info page in the default browser."""

        wbopen(help_page_url)

    def run_checklist(self):
        """A function which runs a fast check and displays the checklist in a window."""

        debug("Running a fast check")
        self.checklist_window = ChecklistWindow()
        self.checklist_window.show()
    
    def change_nameservers(self):
        """A function which changes the nameservers in the resolv.conf file."""

        cd_change_nameservers(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, working_status=self.start_stop_button.text(), nameserver_changer_file_path=nameserver_changer_file_path, tor_nameservers_file_path=tor_nameservers_file_path, original_resolv_configuration_file_path=original_resolv_configuration_file_path, privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path)

    def anonymize_browser(self):
        """A function which anonymizes firefox by changing it's preferences"""
        
        cd_anonymize_browser(user_pwd=user_pwd, init_script_file_path=init_script_file_path, ghostsurf_logo_file_path=ghostsurf_logo_file_path, firefox_profiles_dir=firefox_profiles_dir, custom_firefox_preferences_file_path=custom_firefox_preferences_file_path, firefox_profiles_conf_file_path=firefox_profiles_conf_file_path)
        
    def change_hostname(self):
        """A function which changes the hostname. Note: Modems sees your hostname not your username."""

        cd_change_hostname(user_pwd=user_pwd, hostname_changer_script_file_path=hostname_changer_script_file_path)

    def change_mac_address(self):
        """A function which changes the mac address."""

        cd_change_mac_address(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, mac_changer_script_file_path=mac_changer_script_file_path)

    def ultra_ghost_mode(self):
        """A function which enables/disables ghostsurf at boot."""

        ultra_ghost_mode_status = self.ultra_ghost_button.text()

        if ultra_ghost_mode_status == "disabled":

            debug("Enabling ghostsurf at boot")
            run(["sudo", "-S", start_transparent_proxy_script_file_path], text=True, input=user_pwd)
            run(["sudo", "-S", save_iptables_script_file_path], text=True, input=user_pwd) 
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)       
            config["is_enabled_at_boot"] = "True"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            self.start_stop_button.setText("Stop")
            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')
            self.ultra_ghost_button.setText("enabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")

        else:

            debug("Disabling ghostsurf at boot")
            run(["sudo", "-S", stop_transparent_proxy_script_file_path], text=True, input=user_pwd)
            config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
            config["is_enabled_at_boot"] = "False"
            save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
            self.start_stop_button.setText("Start")
            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')
            self.ultra_ghost_button.setText("disabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")  

    def shred_log_files(self):
        """A function which shreds the log files."""

        cd_shred_logs(ghostsurf_logo_file_path=ghostsurf_logo_file_path, log_shredder_file_path=log_shredder_file_path, current_username=current_username)

    def wipe_memory(self):
        """A function which wipes the memory securely."""

        cd_wipe_memory(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, fast_bomb_script_file_path=fast_bomb_script_file_path, secure_bomb_script_file_path=secure_bomb_script_file_path)

    def reset_settings(self):
        """A function which resets ghostsurf settings."""

        cd_reset(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, reset_iptables_only_script_file_path=reset_iptables_only_script_file_path, reset_script_file_path=reset_script_file_path)



if __name__ == "__main__":

    main()
