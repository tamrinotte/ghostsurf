# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from os import system, path
from pathlib import Path
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from webbrowser import open as wbopen
from time import sleep
from getpass import getuser
from sys import exit as sysexit
from subprocess import run
from threading import Thread

# PySide2
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QLineEdit
from PySide2.QtGui import QPixmap, QIcon, QImage
from PySide2.QtCore import QAbstractListModel, Qt, QRunnable, QThreadPool, QThread, QObject, Signal, Slot

# GUIs
from guis.main_win_ui import Ui_MainWindow
from guis.password_win_ui import Ui_PasswordWindow
from guis.checklist_win_ui import Ui_ChecklistWindow

# Resources
import resources_rc

# Ghostsurf Functions
from gs_functions.check_list_functions import (
    check_fake_hostname_usage, 
    check_fake_mac_address_usage, 
    check_appropriate_nameserver_usage, 
    check_browser_anonymization,
    check_different_timezone_usage,
    check_tor_connection_usage,
)

from gs_functions.control_deck_functions import (
    get_the_public_ip_address,
    kill_log_files,
    reset_ghostsurf_settings,
    change_the_mac_address,
    wipe_the_memory,
    change_the_nameservers,
)

from gs_functions.standard_functions import (
    manage_netfilter_service,
)



# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
# disable(CRITICAL)



##############################

# GLOBAL VARIABLES

##############################

current_username = getuser()
help_page_url = "https://www.github.com/tamrinotte/ghostsurf#readme"
base_dir = path.dirname(__file__)

# CONFIGURATION FILE PATHS

configuration_files_dir_path = Path(base_dir, "configuration_files")
ghostsurf_configuration_file_path = Path(configuration_files_dir_path, "ghostsurf.conf")
privacy_focused_nameservers_file_path = Path(configuration_files_dir_path, "privacy_focused_nameservers_resolv.conf")
tor_nameservers_file_path = Path(configuration_files_dir_path, "tor_nameservers_resolv.conf")
custom_firefox_preferences_file_path = Path(configuration_files_dir_path, "firefox_prefs.js.custom")
original_resolv_configuration_file_path = Path("/etc/resolv.conf")
fake_hostnames_list_file_path = Path(configuration_files_dir_path, "list_of_fake_hostnames.list")
firefox_profiles_conf_file_path = Path(f"/home/{current_username}/.mozilla/firefox/profiles.ini")

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
        
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "You can\'t run this app as the root user"')
        sysexit()

    else:

        app = QApplication([])
        password_window = PasswordWindow()
        password_window.show()
        sysexit(app.exec_())



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
        check_fake_mac_address_usage(user_pwd=user_pwd, checklist_items_dict=checklist_items_dict)
        check_appropriate_nameserver_usage(privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path, original_resolv_configuration_file_path=original_resolv_configuration_file_path, main_window=main_window, checklist_items_dict=checklist_items_dict)
        check_browser_anonymization(current_username=current_username, checklist_items_dict=checklist_items_dict, custom_firefox_preferences_file_path=custom_firefox_preferences_file_path)
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
            open_eye_icon = QIcon()
            open_eye_icon.addPixmap(QPixmap(str(Path(base_dir, "icons", "eye_open.svg"))))
            self.visibility_button.setIcon(open_eye_icon)

        else:

            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            closed_eye_icon = QIcon()
            closed_eye_icon.addPixmap(QPixmap(str(Path(base_dir, "icons", "eye_closed.svg"))))
            self.visibility_button.setIcon(closed_eye_icon)

    def get_user_pwd(self):
        """A function which stores the password that the user entered in a global variable"""
        
        global user_pwd
        user_pwd = self.password_line_edit.text()
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
            warning_dialog.exec_()



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
        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()
    
        with open(ghostsurf_configuration_file_path, "r") as ghostsurf_configuraion_file:
    
            ghostsurf_configuraion_file_contents = ghostsurf_configuraion_file.readlines()

            if "enabled_at_boot=yes\n" in ghostsurf_configuraion_file_contents:

                is_ghostsurf_enabled_at_boot = True

            else:

                is_ghostsurf_enabled_at_boot = False

        if is_ghostsurf_enabled_at_boot == True: 

            self.start_stop_button.setText("Stop")
            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')
            self.ultra_ghost_button.setText("enabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

        self.start_stop_button.pressed.connect(self.start_stop)
        self.my_ip_button.pressed.connect(self.show_my_ip)
        self.status_button.pressed.connect(self.show_status)
        self.change_ip_button.pressed.connect(self.change_id)
        self.info_button.pressed.connect(self.open_info_page) 
        self.pandora_bomb_button.pressed.connect(self.wipe_memory_securely)
        self.ultra_ghost_button.pressed.connect(self.ultra_ghost_mode)
        self.mac_changer_button.pressed.connect(self.change_mac_address)
        self.log_shredder_button.pressed.connect(self.shred_log_files)
        self.reset_button.pressed.connect(self.reset_settings)
        self.dns_changer_button.pressed.connect(self.change_nameservers)
        self.hostname_changer_button.pressed.connect(self.change_hostname)
        self.run_fast_check_button.pressed.connect(self.run_fast_check)
        self.browser_anonymizer_button.pressed.connect(self.anonymize_the_browser)

    def anonymize_the_browser(self):
        """A function which anonymizes firefox by changing it's preferences"""

        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Creating Ghostsurf\'s Firefox profiles"')
        sleep(0.3)
        run(["firefox-esr", "-CreateProfile", "ghostsurf"], text=True, capture_output=True)
        run(["firefox-esr", "-CreateProfile", "penetration-testing"], text=True, capture_output=True)

        if custom_firefox_preferences_file_path.exists() == True:
        
            with open(custom_firefox_preferences_file_path, "r") as the_custom_prefs_file:

                custom_prefs = the_custom_prefs_file.read()

        else:

            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Custom preferences file not found. Try to reinstall ghostsurf!"')

        ghostsurf_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.ghostsurf".format(current_username)], text=True, capture_output=True).stdout.strip(), "user.js")

        with open(ghostsurf_firefox_profile_file_path, "w") as ghostsurf_firefox_profile_user_pref_file:

            ghostsurf_firefox_profile_user_pref_file.write(custom_prefs)

        run(["sudo", "-S", "bash", "-c", "{}".format(init_script_file_path)], input=user_pwd, text=True, capture_output=True)

        with open(firefox_profiles_conf_file_path, "r") as firefox_prof_conf_file:

            firefox_prof_conf_lines = firefox_prof_conf_file.readlines()

        for line in firefox_prof_conf_lines:

            if "Path" in line:

                path = line.split("=")[1][:-1]
                
                if "ghostsurf" in path:

                    ghostsurf_profile_path_spec = path

                elif "default" in path:

                    default_profile_path_spec = path

            elif "Default" in line and "." in line:

                path = line.split("=")[1][:-1]
                default_profile_setting_raw = line

        new_default = f"Default={ghostsurf_profile_path_spec}\n"
        firefox_prof_conf_lines[firefox_prof_conf_lines.index(default_profile_setting_raw)] = new_default

        with open(firefox_profiles_conf_file_path, "w") as f:

            f.write("".join(firefox_prof_conf_lines))

        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Ghostsurf\'s Firefox profiles are created. And, preferences are set."')

    def run_fast_check(self):
        """A function which runs a fast check and displays the checklist in a window."""

        debug("Running a fast check")

        self.checklist_window = ChecklistWindow()

        self.checklist_window.show()

    def change_hostname(self):
        """A function which changes the hostname. Note: Modems sees your hostname not your username."""

        question_dialog = QMessageBox()
        question_dialog.setIcon(QMessageBox.Question)
        question_dialog.setWindowTitle("Important")
        question_dialog.setText("This operation requires reboot. Do you allow to reboot this system?")
        question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        question_dialog_answer = question_dialog.exec_()

        if question_dialog_answer == QMessageBox.Yes:

            debug("Rebooting the system")
            run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)
            run(["sudo", "-S", "bash", "-c", "{}".format(hostname_changer_script_file_path)], input=user_pwd, text=True, capture_output=True)
            run(["sudo", "reboot"], input=user_pwd, text=True, capture_output=True)

        else:

            debug("Operation canceled")

    def change_nameservers(self):
        """A function which changes the nameservers in the resolv.conf file."""

        change_the_nameservers(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, working_status=self.start_stop_button.text(), nameserver_changer_file_path=nameserver_changer_file_path, tor_nameservers_file_path=tor_nameservers_file_path, original_resolv_configuration_file_path=original_resolv_configuration_file_path, privacy_focused_nameservers_file_path=privacy_focused_nameservers_file_path)

    def reset_settings(self):
        """A function which resets ghostsurf settings."""

        reset_ghostsurf_settings(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, reset_iptables_only_script_file_path=reset_iptables_only_script_file_path, reset_script_file_path=reset_script_file_path)

    def shred_log_files(self):
        """A function which shreds the log files."""

        kill_log_files(ghostsurf_logo_file_path=ghostsurf_logo_file_path, log_shredder_file_path=log_shredder_file_path, current_username=current_username)

    def change_mac_address(self):
        """A function which changes the mac address."""
        
        change_the_mac_address(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, mac_changer_script_file_path=mac_changer_script_file_path)

    def ultra_ghost_mode(self):
        """A function which enables/disables ghostsurf at boot."""

        ultra_ghost_mode_status = self.ultra_ghost_button.text()

        if ultra_ghost_mode_status == "disabled":

            debug("Enabling ghostsurf at boot")
            run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)
            run(["sudo", "-S", "bash", "-c", "{}".format(save_iptables_script_file_path)], input=user_pwd, text=True, capture_output=True)

            with open(ghostsurf_configuration_file_path, "r") as a:

                a_contents = a.readlines()
                    
                if "enabled_at_boot=no\n" in a_contents:
                    line_index = a_contents.index("enabled_at_boot=no\n")
                    a_contents[line_index]="enabled_at_boot=yes\n"
                    debug(a_contents)

            with open(ghostsurf_configuration_file_path, "w") as b:

                b.write(''.join(a_contents))

            self.start_stop_button.setText("Stop")
            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')
            self.ultra_ghost_button.setText("enabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")

        else:

            debug("Disabling ghostsurf at boot")
            run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

            with open(ghostsurf_configuration_file_path, "r") as a:
                
                a_contents = a.readlines()

                if "enabled_at_boot=yes\n" in a_contents:
                    
                    line_index = a_contents.index("enabled_at_boot=yes\n")
                    a_contents[line_index]="enabled_at_boot=no\n"

            with open(ghostsurf_configuration_file_path, "w") as b:
                
                b.write(''.join(a_contents))

            self.start_stop_button.setText("Start")
            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')
            self.ultra_ghost_button.setText("disabled")
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")  

    def wipe_memory_securely(self):
        """A function which wipes the memory securely."""

        wipe_the_memory(user_pwd=user_pwd, ghostsurf_logo_file_path=ghostsurf_logo_file_path, fast_bomb_script_file_path=fast_bomb_script_file_path, secure_bomb_script_file_path=secure_bomb_script_file_path)

    def open_info_page(self):
        """A function which opens the info page in the default browser."""

        wbopen(help_page_url)

    def start_stop(self):
        """A function which redirects all internet traffic over tor."""

        def start_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the start button is pressed to identify what app should do."""

            user_answer = i.text()

            if user_answer == "&Yes":

                debug("Yes button is clicked")
                run(["sudo", "-S", "bash", "-c", "{}".format(init_script_file_path)], input=user_pwd, text=True, capture_output=True)
                run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)
                self.start_stop_button.setText("Stop")

            elif user_answer == "&No":

                debug("No button is clicked")
                run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)
                self.start_stop_button.setText("Stop")

            else:

                debug("Operation canceled")

        def stop_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the stop button is pressed to identify what app should do."""

            user_answer = i.text()

            if user_answer == "&Yes":

                run(["sudo", "-S", "bash", "-c", "{}".format(init_script_file_path)], input=user_pwd, text=True, capture_output=True)
                run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                with open(ghostsurf_configuration_file_path, "r") as d:

                    d_contents = d.readlines()

                    if "enabled_at_boot=yes\n" in d_contents:
                        
                        line_index = d_contents.index("enabled_at_boot=yes\n")
                        d_contents[line_index] = "enabled_at_boot=no\n"

                with open(ghostsurf_configuration_file_path, "w") as e:

                    e.write("\n".join(d_contents))

                self.start_stop_button.setText("Start")
                self.ultra_ghost_button.setText("disabled")
                self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")

            elif user_answer == "&No":

                run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                with open(ghostsurf_configuration_file_path, "r") as d:

                    d_contents = d.readlines()

                    if "enabled_at_boot=yes\n" in d_contents:
                        
                        line_index = d_contents.index("enabled_at_boot=yes\n")
                        d_contents[line_index] = "enabled_at_boot=no\n"

                with open(ghostsurf_configuration_file_path, "w") as e:

                    e.write("\n".join(d_contents))

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
            question_dialog.exec_()
            
        else:

            debug("Stop button pressed")
            question_dialog = QMessageBox()
            question_dialog.setIcon(QMessageBox.Question)
            question_dialog.setWindowTitle("Important")
            question_dialog.setText("Are you allowing to killing of dangerous applications and cleaning of dangerous caches?")
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            question_dialog.buttonClicked.connect(stop_button_question_dialog_processor)
            question_dialog.exec_() 

        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')

        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def show_my_ip(self):
        """A function which shows your public ip address."""
        
        public_ip_thread = Thread(target=get_the_public_ip_address, args=[user_pwd, ghostsurf_logo_file_path])
        public_ip_thread.start()

    def show_status(self):
        """A function which shows the tor service's status."""

        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        if "inactive" in tor_status:

            self.status_label.setStyleSheet(u"#status_label {color: red;}")
            self.status_label.setText('Inactive')
        
        else:

            self.status_label.setStyleSheet(u"#status_label {color: green;}")
            self.status_label.setText('Active')

    def change_id(self):
        """A function which changes your ip address by restarting the transparent proxy."""

        run(["sudo", "-S", "bash", "-c", "systemctl restart tor"], input=user_pwd, text=True, capture_output=True)



if __name__ == "__main__":

    main()
