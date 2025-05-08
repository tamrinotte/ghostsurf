# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from pathlib import Path
from webbrowser import open as wbopen
from time import sleep
from getpass import getuser
from sys import argv, exit as sysexit
from subprocess import run, check_call, CalledProcessError
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
from modules.gui_control_deck import (
    gui_cd_show_ip,
    gui_cd_shred_logs,
    gui_cd_reset,
    gui_cd_change_mac_address,
    gui_cd_wipe_memory,
    gui_cd_change_nameservers,
    gui_cd_anonymize_browser,
    gui_cd_change_hostname,
)
from modules.json_config_loading import (
    load_ghostsurf_config,
    save_ghostsurf_config,
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
from modules.logging_config import (
    debug,
    info,
    warning,
    error,
)
from modules.notification_config import display_notification



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
ghostsurf_logo_file_path = str(Path(icons_dir_path, "ghostsurf.png"))

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

    if current_username == "root":

        display_notification(
            icon_file_path=ghostsurf_logo_file_path,
            message="You can't run this app as the root user."
        )
        sysexit()

    else:

        if len(argv) == 1:
        
            app = QApplication([])
            main_window = MainWindow()
            main_window.show()
            sysexit(app.exec())

        else:

            parser = argparse.ArgumentParser(description='GhostSurf CLI')
            subparsers = parser.add_subparsers(dest='command')
            start_parser = subparsers.add_parser('start', help='Start transparent proxy')
            start_parser.set_defaults(
                func=lambda: tui_cd_start_transparent_proxy(
                    init_script_file_path,
                    start_transparent_proxy_script_file_path,
                    ghostsurf_settings_file_path
                )
            )
            stop_parser = subparsers.add_parser('stop', help='Stop transparent proxy')
            stop_parser.set_defaults(
                func=lambda: tui_cd_stop_transparent_proxy(
                    init_script_file_path,
                    stop_transparent_proxy_script_file_path,
                    ghostsurf_settings_file_path
                )
            )
            change_ip_parser = subparsers.add_parser('changeip', help="Change my IP")
            change_ip_parser.set_defaults(func=tui_cd_change_ip)
            my_ip_parser = subparsers.add_parser('myip', help="Show my public IP address")
            my_ip_parser.set_defaults(func=tui_cd_show_ip)
            status_parser = subparsers.add_parser('status', help="Show if transparent proxy is on/off")
            status_parser.set_defaults(func=lambda: tui_cd_show_status(ghostsurf_settings_file_path))
            change_mac_parser = subparsers.add_parser('changemac', help="Change my mac address")
            change_mac_parser.set_defaults(func=lambda: tui_cd_change_mac_address(mac_changer_script_file_path))
            change_dns_parser = subparsers.add_parser('changedns', help="Change my DNS")
            change_dns_parser.set_defaults(
                func=lambda: tui_cd_change_dns(
                    nameserver_changer_file_path,
                    tor_nameservers_file_path,
                    original_resolv_configuration_file_path,
                    privacy_focused_nameservers_file_path,
                    ghostsurf_settings_file_path
                )
            )
            change_hostname = subparsers.add_parser('changehostname', help="Change my hostname")
            change_hostname.set_defaults(func=lambda: tui_cd_change_hostname(hostname_changer_script_file_path))
            white_rabbit_parser = subparsers.add_parser('whiterabbit', help="Follow the white rabbit")
            white_rabbit_parser.set_defaults(func=lambda: tui_cd_display_the_help_page(help_page_url))
            pandora_bomb_parser = subparsers.add_parser('pandorabomb', help="Wipe the RAM")
            pandora_bomb_parser.set_defaults(
                func=lambda: tui_cd_wipe_memory(
                    fast_bomb_script_file_path,
                    secure_bomb_script_file_path
                )
            )
            browser_anonymization_parser = subparsers.add_parser('anonymizebrowser', help="Anonymize firefox")
            browser_anonymization_parser.set_defaults(
                func=lambda: tui_cd_anonymize_browser(
                    firefox_profiles_dir,
                    custom_firefox_preferences_file_path,
                    init_script_file_path,
                    firefox_profiles_conf_file_path
                )
            )
            log_shedder_parser = subparsers.add_parser('shredlogs', help="Shred log files")
            log_shedder_parser.set_defaults(func=lambda: tui_cd_shred_logs(log_shredder_file_path, current_username))
            checklist_parser = subparsers.add_parser('checklist', help="Run anonymity checklist")
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
            reset_parser = subparsers.add_parser('reset', help="Reset changes")
            reset_parser.set_defaults(
                func=lambda: tui_cd_reset(
                    reset_iptables_only_script_file_path,
                    reset_script_file_path
                )
            )
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
        tor_status = run(
            ["systemctl", "status", "tor"],
            text=True,
            capture_output=True
        ).stdout.strip()

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
        self.log_shredder_button.pressed.connect(self.shred_log_files)
        self.pandora_bomb_button.pressed.connect(self.wipe_memory)
        self.reset_button.pressed.connect(self.reset_settings)

    def start_stop(self):

        def start_button_question_dialog_processor(i):

            debug("Start transparent proxy button has been pressed.")
            user_answer = i.text()

            if user_answer == "&Yes":

                debug("No button is clicked")
                try:

                    check_call(["pkexec", "bash", "-c", f"{init_script_file_path} && {start_transparent_proxy_script_file_path}"])

                except CalledProcessError as e:

                    error(f"Error: {e}")
                    return

                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "True"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Stop")

            elif user_answer == "&No":

                debug("No button is clicked")
                try:
                    
                    check_call(["pkexec", start_transparent_proxy_script_file_path])
                
                except CalledProcessError as e:
                
                    debug(f"Error: {e}")
                    return

                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "True"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Stop")

            else:

                debug("Operation canceled")

        def stop_button_question_dialog_processor(i):

            debug("Stop transparent proxy button has been pressed.")
            user_answer = i.text()

            if user_answer == "&Yes":

                try:

                    check_call(["pkexec", "bash", "-c", f"{init_script_file_path} && {stop_transparent_proxy_script_file_path}"])

                except CalledProcessError as e:

                    error(f"Error: {e}")
                    return

                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Start")

            elif user_answer == "&No":

                try:

                    check_call(["pkexec", stop_transparent_proxy_script_file_path])

                except CalledProcessError as e:

                    error(f"Error: {e}")
                    return

                config = load_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path)
                config["is_ghostsurf_on"] = "False"
                save_ghostsurf_config(ghostsurf_settings_file_path=ghostsurf_settings_file_path, config=config)
                self.start_stop_button.setText("Start")

            else:

                debug("Operation canceled")

        if self.start_stop_button.text() == "Start":

            debug("Start button pressed")
            question_dialog = QMessageBox()
            question_dialog.setIcon(QMessageBox.Question)
            question_dialog.setWindowTitle("Important")
            question_dialog.setText(
                "Are you allowing to killing of dangerous applications and cleaning of dangerous caches?"
            )
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            question_dialog.buttonClicked.connect(start_button_question_dialog_processor)
            question_dialog.exec()

        else:

            debug("Stop button pressed")
            question_dialog = QMessageBox()
            question_dialog.setIcon(QMessageBox.Question)
            question_dialog.setWindowTitle("Important")
            question_dialog.setText(
                "Are you allowing to killing of dangerous applications and cleaning of dangerous caches?"
            )
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            question_dialog.buttonClicked.connect(stop_button_question_dialog_processor)
            question_dialog.exec() 

        tor_status = run(
            ["systemctl", "status", "tor"],
            text=True,
            capture_output=True
        ).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def show_ip(self):

        public_ip_thread = Thread(target=gui_cd_show_ip, args=[ghostsurf_logo_file_path])
        public_ip_thread.start()

    def show_status(self):

        tor_status = run(
            ["systemctl", "status", "tor"],
            text=True,
            capture_output=True
        ).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def change_ip(self):

        debug("Change IP button has been clicked!")
        run(["pkexec", "systemctl", "restart", "tor"], text=True)

    def display_the_help_page(self):

        wbopen(help_page_url)

    def run_checklist(self):

        debug("Running a fast check")
        self.checklist_window = ChecklistWindow()
        self.checklist_window.show()
    
    def change_nameservers(self):

        gui_cd_change_nameservers(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            working_status=self.start_stop_button.text(),
            nameserver_changer_file_path=nameserver_changer_file_path,
            tor_nameservers_file_path=tor_nameservers_file_path,
            original_resolv_configuration_file_path=original_resolv_configuration_file_path,
            privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path
        )

    def anonymize_browser(self):
        
        gui_cd_anonymize_browser(
            init_script_file_path=init_script_file_path,
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            firefox_profiles_dir=firefox_profiles_dir,
            custom_firefox_preferences_file_path=custom_firefox_preferences_file_path,
            firefox_profiles_conf_file_path=firefox_profiles_conf_file_path
        )
        
    def change_hostname(self):

        gui_cd_change_hostname(
            hostname_changer_script_file_path=hostname_changer_script_file_path
        )

    def change_mac_address(self):

        gui_cd_change_mac_address(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            mac_changer_script_file_path=mac_changer_script_file_path
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
            secure_bomb_script_file_path=secure_bomb_script_file_path
        )

    def reset_settings(self):

        gui_cd_reset(
            ghostsurf_logo_file_path=ghostsurf_logo_file_path,
            reset_iptables_only_script_file_path=reset_iptables_only_script_file_path,
            reset_script_file_path=reset_script_file_path
        )



if __name__ == "__main__":

    main()