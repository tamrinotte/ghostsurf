# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from pathlib import Path
from webbrowser import open as wbopen
from time import sleep
from getpass import getuser
from sys import argv, exit as sysexit
from subprocess import run
from argparse import ArgumentParser

# PySide6
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
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
from ui.checklist_win_ui import Ui_ChecklistWindow

# Resources
import resources_rc

# Ghostsurf Modules
from modules.integrity_checker import check_root_privileges, validate_ghostsurf_paths
from modules.conf_ghostsurf import (
    load_ghostsurf_config,
)
from modules.conf_logging import (
    info,
    error,
)
from modules.gui_control_deck import (
    gui_cd_start_stop_transparent_proxy,
    gui_cd_update_tor_status_label,
    gui_cd_change_ip,
    gui_cd_show_ip,
    gui_cd_shred_logs,
    gui_cd_reset,
    gui_cd_change_mac_address,
    gui_cd_wipe_memory,
    gui_cd_change_nameservers,
    gui_cd_anonymize_browser,
    gui_cd_change_hostname,
    gui_update_start_stop_button_text,
)
from modules.tui_control_deck import (
    tui_cd_start_transparent_proxy,
    tui_cd_stop_transparent_proxy,
    tui_cd_change_ip,
    tui_cd_show_ip,
    tui_cd_show_status,
    tui_cd_change_mac_address,
    tui_cd_change_dns,
    tui_cd_change_hostname,
    tui_cd_display_the_help_page,
    tui_cd_anonymize_browser,
    tui_cd_wipe_memory,
    tui_cd_shred_logs,
    tui_cd_checklist,
    tui_cd_reset,
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

# BASH SCRIPT FILE PATHS
bash_scripts_dir_path = Path(base_dir, "bash_scripts")
mac_changer_script_file_path = Path(bash_scripts_dir_path, "mac_changer.sh")
fast_bomb_script_file_path = Path(bash_scripts_dir_path, "fast_bomb.sh")
secure_bomb_script_file_path = Path(bash_scripts_dir_path, "secure_bomb.sh")
reset_script_file_path = Path(bash_scripts_dir_path, "reset.sh")
start_transparent_proxy_script_file_path = Path(bash_scripts_dir_path, "start_transparent_proxy.sh")
stop_transparent_proxy_script_file_path = Path(bash_scripts_dir_path, "stop_transparent_proxy.sh")
hostname_changer_script_file_path = Path(bash_scripts_dir_path, "hostname_changer.sh")
init_script_file_path = Path(bash_scripts_dir_path, "init.sh")
log_shredder_file_path = Path(bash_scripts_dir_path, "log_shredder.sh")
nameserver_changer_file_path = Path(bash_scripts_dir_path, "nameservers_changer.sh")

# BACKUP FILE PATHS
backup_files_dir = Path(base_dir, "backup_files")
timezone_backup_file_path = Path(backup_files_dir, "timezone.backup")

# ICON FILE PATHS
icons_dir_path = Path(base_dir, "icons")
ghostsurf_logo_file_path = str(Path(icons_dir_path, "ghostsurf.png"))
tick = QImage(str(Path(icons_dir_path, "tick.png")))
cross = QImage(str(Path(icons_dir_path, "cross.png")))

# PATHS TO VALIDATE
paths_to_check = {
    "Ghostsurf logo": ghostsurf_logo_file_path,
    "Settings file": ghostsurf_settings_file_path,
    "MAC changer script": mac_changer_script_file_path,
    "Log shredder script": log_shredder_file_path,
    "Fast bomb script": fast_bomb_script_file_path,
    "Secure bomb script": secure_bomb_script_file_path,
    "Reset script": reset_script_file_path,
    "Start proxy script": start_transparent_proxy_script_file_path,
    "Stop proxy script": stop_transparent_proxy_script_file_path,
    "Hostname changer script": hostname_changer_script_file_path,
    "Init script": init_script_file_path,
    "Nameserver changer script": nameserver_changer_file_path,
    "Timezone backup": timezone_backup_file_path,
    "Privacy DNS config": privacy_focused_nameservers_file_path,
    "Tor DNS config": tor_nameservers_file_path,
    "Firefox profiles.ini": firefox_profiles_conf_file_path,
    "Firefox prefs file": custom_firefox_preferences_file_path,
    "Fake hostname list": fake_hostnames_list_file_path,
}

##############################

# THE MAIN FUNCTION

##############################

def main():
    is_using_gui = len(argv) == 1
    check_root_privileges()
    validate_ghostsurf_paths(paths_dict=paths_to_check)

    if is_using_gui:
        app = QApplication([])
        main_window = MainWindow()
        main_window.show()
        sysexit(app.exec())
    else:
        parser = ArgumentParser(description='GhostSurf CLI')
        subparsers = parser.add_subparsers(dest='command')
        start_parser = subparsers.add_parser('start', help='Start the transparent proxy')
        start_parser.set_defaults(
            func=lambda: tui_cd_start_transparent_proxy(
                init_script_file_path,
                start_transparent_proxy_script_file_path,
                ghostsurf_settings_file_path
            )
        )
        stop_parser = subparsers.add_parser('stop', help='Stop the transparent proxy')
        stop_parser.set_defaults(
            func=lambda: tui_cd_stop_transparent_proxy(
                init_script_file_path,
                stop_transparent_proxy_script_file_path,
                ghostsurf_settings_file_path
            )
        )
        change_ip_parser = subparsers.add_parser('changeip', help="Change your public IP address")
        change_ip_parser.set_defaults(func=tui_cd_change_ip)
        my_ip_parser = subparsers.add_parser('myip', help="Display your current public IP address")
        my_ip_parser.set_defaults(func=tui_cd_show_ip)
        status_parser = subparsers.add_parser('status', help="Show the status of the transparent proxy")
        status_parser.set_defaults(func=lambda: tui_cd_show_status(ghostsurf_settings_file_path))
        change_mac_parser = subparsers.add_parser('changemac', help="Change your MAC address")
        change_mac_parser.set_defaults(func=lambda: tui_cd_change_mac_address(mac_changer_script_file_path))
        change_dns_parser = subparsers.add_parser('changedns', help="Change your DNS nameservers")
        change_dns_parser.set_defaults(
            func=lambda: tui_cd_change_dns(
                nameserver_changer_file_path,
                tor_nameservers_file_path,
                original_resolv_configuration_file_path,
                privacy_focused_nameservers_file_path,
                ghostsurf_settings_file_path
            )
        )
        change_hostname = subparsers.add_parser('changehostname', help="Change your system hostname")
        change_hostname.set_defaults(func=lambda: tui_cd_change_hostname(hostname_changer_script_file_path))
        white_rabbit_parser = subparsers.add_parser('whiterabbit', help="Open the GhostSurf GitHub documentation page")
        white_rabbit_parser.set_defaults(func=lambda: tui_cd_display_the_help_page(help_page_url))
        pandora_bomb_parser = subparsers.add_parser('pandorabomb', help="Wipe system memory (RAM)")
        pandora_bomb_parser.set_defaults(
            func=lambda: tui_cd_wipe_memory(
                fast_bomb_script_file_path,
                secure_bomb_script_file_path
            )
        )
        browser_anonymization_parser = subparsers.add_parser('anonymizebrowser', help="Create and anonymize Firefox profiles")
        browser_anonymization_parser.set_defaults(
            func=lambda: tui_cd_anonymize_browser(
                firefox_profiles_dir,
                custom_firefox_preferences_file_path,
                init_script_file_path,
                firefox_profiles_conf_file_path
            )
        )
        log_shedder_parser = subparsers.add_parser('shredlogs', help="Securely delete log files")
        log_shedder_parser.set_defaults(func=lambda: tui_cd_shred_logs(log_shredder_file_path, current_username))
        checklist_parser = subparsers.add_parser('checklist', help="Run the anonymity checklist")
        checklist_parser.set_defaults(
            func=lambda: tui_cd_checklist(
                fake_hostnames_list_file_path,
                privacy_focused_nameservers_file_path,
                original_resolv_configuration_file_path,
                current_username,
                firefox_profiles_dir,
                custom_firefox_preferences_file_path,
                timezone_backup_file_path,
                ghostsurf_settings_file_path
            )
        )
        reset_parser = subparsers.add_parser('reset', help="Revert all changes and restore defaults")
        reset_parser.set_defaults(func=lambda: tui_cd_reset(reset_script_file_path))
        args = parser.parse_args()

        if hasattr(args, 'func'):
            args.func()
        else:
            parser.print_help()

##############################

# WORKERS

##############################

class CheckListWorkerSignals(QObject):
    list_item = Signal(str)

class CheckListWorker(QRunnable):
    def __init__(self):
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
    }

    @Slot()
    def run(self):
        check_fake_hostname_usage(
            fake_hostnames_list_file_path=fake_hostnames_list_file_path,
            checklist_items_dict=checklist_items_dict,
        )
        check_fake_mac_address_usage(checklist_items_dict=checklist_items_dict)
        check_appropriate_nameserver_usage(
            privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path,
            original_resolv_configuration_file_path=original_resolv_configuration_file_path,
            checklist_items_dict=checklist_items_dict,
            ghostsurf_settings_file_path=ghostsurf_settings_file_path,
        )
        check_browser_anonymization(
            current_username=current_username,
            checklist_items_dict=checklist_items_dict,
            firefox_profiles_dir=firefox_profiles_dir,
            custom_firefox_preferences_file_path=custom_firefox_preferences_file_path,
        )
        check_different_timezone_usage(
            timezone_backup_file_path=timezone_backup_file_path,
            checklist_items_dict=checklist_items_dict,
        )
        check_tor_connection_usage(checklist_items_dict=checklist_items_dict)

        for key in checklist_items_dict.keys():
            self.signals.list_item.emit(key)
            sleep(0.02)

##############################

# DATA MODELS

##############################

class ChecklistModel(QAbstractListModel):
    def __init__(self, list_items=None): # list_items=None is a default value
        super().__init__()
        self.list_items = list_items or []

    def data(self, index, role):
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
        return len(self.list_items)

##############################

# CHECK LIST WINDOW

##############################

class ChecklistWindow(QWidget, Ui_ChecklistWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = ChecklistModel()
        self.threadpool = QThreadPool()
        self.checklist_list_view.setModel(self.model)
        worker = CheckListWorker()
        worker.signals.list_item.connect(self.run_all_the_checks)
        self.threadpool.start(worker)

    def run_all_the_checks(self, key):
        self.model.list_items.append((checklist_items_dict[key], key))
        self.model.layoutChanged.emit()

##############################

# MAIN WINDOW

##############################

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        ghostsurf_config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
        gui_cd_update_tor_status_label(
            label_widget=self.status_label,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
        )
        gui_update_start_stop_button_text(
            button_widget=self.start_stop_button,
            ghostsurf_settings_file_path=ghostsurf_settings_file_path,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
        )
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
        self.log_shredder_button.pressed.connect(self.shred_log_files)
        self.pandora_bomb_button.pressed.connect(self.wipe_memory)
        self.reset_button.pressed.connect(self.reset_settings)

    def start_stop(self):
        gui_cd_start_stop_transparent_proxy(
            init_script_file_path=init_script_file_path,
            start_transparent_proxy_script_file_path=start_transparent_proxy_script_file_path,
            stop_transparent_proxy_script_file_path=stop_transparent_proxy_script_file_path,
            button_label_widget=self.start_stop_button,
            status_label_widget=self.status_label,
            ghostsurf_settings_file_path=ghostsurf_settings_file_path,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
        )

    def show_ip(self):
        gui_cd_show_ip(ghostsurf_logo_file_path=ghostsurf_logo_file_path)

    def show_status(self):
        gui_cd_update_tor_status_label(
            label_widget=self.status_label,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
        )

    def change_ip(self):
        gui_cd_change_ip(ghostsurf_logo_file_path=ghostsurf_logo_file_path)

    def display_the_help_page(self):
        wbopen(help_page_url)

    def run_checklist(self):
        self.checklist_window = ChecklistWindow()
        self.checklist_window.show()
    
    def change_nameservers(self):
        gui_cd_change_nameservers(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            working_status=self.start_stop_button.text(),
            nameserver_changer_file_path=nameserver_changer_file_path,
            tor_nameservers_file_path=tor_nameservers_file_path,
            original_resolv_configuration_file_path=original_resolv_configuration_file_path,
            privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path,
        )

    def anonymize_browser(self):
        gui_cd_anonymize_browser(
            init_script_file_path=init_script_file_path,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            firefox_profiles_dir=firefox_profiles_dir,
            custom_firefox_preferences_file_path=custom_firefox_preferences_file_path,
            firefox_profiles_conf_file_path=firefox_profiles_conf_file_path,
        )
        
    def change_hostname(self):
        gui_cd_change_hostname(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            hostname_changer_script_file_path=hostname_changer_script_file_path,
        )

    def change_mac_address(self):
        gui_cd_change_mac_address(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            mac_changer_script_file_path=mac_changer_script_file_path,
        )

    def shred_log_files(self):
        gui_cd_shred_logs(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            log_shredder_file_path=log_shredder_file_path,
            current_username=current_username,
        )

    def wipe_memory(self):
        gui_cd_wipe_memory(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            fast_bomb_script_file_path=fast_bomb_script_file_path,
            secure_bomb_script_file_path=secure_bomb_script_file_path,
        )

    def reset_settings(self):
        gui_cd_reset(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            reset_script_file_path=reset_script_file_path,
        )

if __name__ == "__main__":
    main()