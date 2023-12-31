# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from os import system, popen, path
from pathlib import Path
from logging import basicConfig, DEBUG, debug, disable, CRITICAL
from webbrowser import open as wbopen
from threading import Thread
from re import compile
from time import sleep
from getpass import getuser
from pathlib import Path
from socket import gethostname
from sys import exit as sysexit
from subprocess import run

# PySide2
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QLineEdit, QListView, QVBoxLayout
from PySide2.QtGui import QPixmap, QIcon, QImage
from PySide2.QtCore import QAbstractListModel, Qt, QRunnable, QThreadPool, QThread, QObject, Signal, Slot

# Guis
from guis.main_win_ui import Ui_MainWindow
from guis.password_win_ui import Ui_PasswordWindow
from guis.checklist_win_ui import Ui_ChecklistWindow

# Resources
import resources_rc

# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)

# GLOBAL VARIABLES

# Getting the username of the user who started this application
current_username = getuser()
    
# Creating a string which is equal to this application's help page url
help_page_url = "https://www.github.com/tamrinotte/ghostsurf#readme"

# Creating a variable called base_dir which leads to the current working directory.
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


def main():
    """The function which runs the entire application"""

    # Checking if the current_username is equal to root
    if current_username == "root":
        
        # Sending notification to let the user know that the application is trying to connect to the server
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "You can\'t run this app as the root user"')

        # Exiting the system
        sysexit()

    # Checking if the current_username is not equal to root
    else:

        # Creating an app object from QApplication
        app = QApplication([])

        # Creating a password_window object from PasswordWindow class
        password_window = PasswordWindow()

        # Showing the password window
        password_window.show()

        # Executing the app
        sysexit(app.exec_())


def check_fake_hostname_usage():
    """A function which checks the hostname"""

    # Opening the list_of_fake_hostnames file in reading mode 
    with open(fake_hostnames_list_file_path, "r") as fake_hostnames_file:

        # Creating a list of fake hostnames from the fake_hostnames_file's lines
        list_of_fake_hostnames = fake_hostnames_file.readlines()

    # Getting the current hostname
    current_hostname = gethostname()

    # Checking if the current hostname is in the list of fake hostnames
    if f'{current_hostname}\n' in list_of_fake_hostnames:

        # Updating the 'Using fake hostname' key's value pair to True
        checklist_items_dict['Using fake hostname'] = True


def check_fake_mac_address_usage():
    """A function which checks wheather or not you are using fake mac address"""

    # Getting the active network adaptor's name
    list_of_network_interfaces = run(["sudo", "-S",  "bash", "-c", "ip -o link show | awk -F': ' '{print $2}'"], input=user_pwd, text=True, capture_output=True).stdout.strip("\n\r").split("\n")

    verification_list = []

    for interface in list_of_network_interfaces:

        interface = interface.strip("\n\r")

        if interface != "lo":

            debug(f"Network Interface Name = {interface}")

            # Getting mac address information
            mac_address_info = popen(f'macchanger -s {interface}').read().split("\n")[:-1]

            # Getting the permanent mac address
            permanent_mac_address = mac_address_info[1].split(" ")[2].strip()

            # Getting the current mac address
            current_mac_address = mac_address_info[0].split(" ")[4].strip()

            # Printing the permanent mac address and the current mac address in debug mode.
            debug(f'Permanent Mac Address = {permanent_mac_address}\nCurrent Mac Address = {current_mac_address}')

            # Checking if the current mac address is not equal to the permanent mac address
            if current_mac_address != permanent_mac_address:

                verification_list.append(True)

                if verification_list.count(True) == len(list_of_network_interfaces) -1:

                    # Setting the 'Using fake mac address' key's value pair to True
                    checklist_items_dict['Using fake mac address'] = True

                else:

                    # Setting the 'Using fake mac address' key's value pair to False
                    checklist_items_dict['Using fake mac address'] = False

            else:

                verification_list.append(False)

                # Setting the 'Using fake mac address' key's value pair to False
                checklist_items_dict['Using fake mac address'] = False


def check_appropriate_nameserver_usage():
    """A function which checks if you are using privacy focused name servers"""

    # Opening the privacy_focused_nameservers_resolv.conf file in reading mode as privacy_focused_nameservers_file
    with open(privacy_focused_nameservers_file_path, "r") as privacy_focused_nameservers_file:

        # Reading privacy_focused_nameservers_file's lines
        privacy_focused_nameservers = privacy_focused_nameservers_file.read().strip('\n\r')

    # Creating a variable that holds the tor nameserver specification 
    tor_nameserver = "nameserver 127.0.0.1"

    # Opening the resolv.conf file in reading mode as resolv_conf_file
    with open(original_resolv_configuration_file_path, "r") as resolv_conf_file:

        # Reading resolv_conf_file's contents
        resolv_conf_file_contents = resolv_conf_file.read().strip('\n\r')

    debug(f'Start stop button\'s text = {main_window.start_stop_button.text()}')

    debug(f'Privacy Focused Nameservers = {privacy_focused_nameservers}\nResolv.conf File = {resolv_conf_file_contents}\nTor Nameserver = {tor_nameserver}')

    # Checking if start_stop_button's text in the main window is equal to Start string.
    if main_window.start_stop_button.text() == "Start":

        # Checking if resolv_conf_file_contents is equal to privacy_focused_nameservers
        if resolv_conf_file_contents == privacy_focused_nameservers:

            # Setting the 'Using appropriate nameservers' key's value pair to True
            checklist_items_dict['Using appropriate nameservers'] = True

    # Checking if start_stop_button's text in the main window is not equal to Start string.
    else:

        if resolv_conf_file_contents == tor_nameserver:

            # Setting the 'Using appropriate nameservers' key's value pair to True
            checklist_items_dict['Using appropriate nameservers'] = True


def check_browser_anonymization():
    """A function which checks if browser anonymization preferences are in use"""

    ghostsurf_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.ghostsurf".format(current_username)], text=True, capture_output=True).stdout.strip(), "user.js")
    
    penetration_testing_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.penetration-testing".format(current_username)], text=True, capture_output=True).stdout.strip())

    if ghostsurf_firefox_profile_file_path.exists() == True and custom_firefox_preferences_file_path.exists() == True and penetration_testing_firefox_profile_file_path.exists() == True:

        with open(custom_firefox_preferences_file_path, "r") as cfpfp:

            cfpfp_contents = cfpfp.read()

        with open(ghostsurf_firefox_profile_file_path, "r") as gfpfp:

            gfpfp_contents = gfpfp.read()

        debug(f'Custom Firefox Preferences File Path Content = {cfpfp_contents}\nGhostsurf Firefox Profile File Path Content = {gfpfp_contents}')
        
        # Setting the 'Ghostsurf\'s Firefox profiles are available. And, preferences are set' key's value pair to True
        checklist_items_dict['Ghostsurf\'s Firefox profiles are available. And, preferences are set'] = bool(cfpfp_contents == gfpfp_contents)

    else:

        debug('Couldn\'t find a path')


def check_different_timezone_usage():
    """A function which checks if a different timezone is set in the system"""

    # Opening the file in timezone_backup_file_path in reading mode with original_timezone_file name
    with open(timezone_backup_file_path, "r") as original_timezone_file:

        # Reading the file's contents
        otf_content = original_timezone_file.read().strip()

    # Getting the current timezone using system commands
    current_timezone = popen("timedatectl show | grep Timezone | sed 's/Timezone=//g'").read().strip()

    # Creating a boolean by checking if otf_content is not equal to current_timezone
    is_timezone_different = bool(otf_content!=current_timezone)
    
    # Printing the original timezone, current time zone and the is_timezone_different variable's value in debug mode
    debug(f'Original Timezone = {otf_content}\nCurrent Timezone = {current_timezone}\nIs Timezone Different = {is_timezone_different}')

    # Setting the 'Using different timezone' key's value pair to True
    checklist_items_dict['Using different timezone'] = is_timezone_different


def check_tor_connection_usage():
    """A function which checks if a transparent proxy is working."""

    # Sending a get request to https://check.torproject.org to learn if transparent proxy set correctly
    tor_connection_status = str(popen(f'curl -s https://check.torproject.org/ | grep -q Congratulations && echo "Connected through Tor" || echo "Not connected through Tor"').read()).strip()

    # Creaing a boolean
    is_transparent_proxy_set_correctly = bool(tor_connection_status=="Connected through Tor")

    # Printing if transparent proxy set correctly in debug mode
    debug(f'Check Tor Project Result = {tor_connection_status}\nIs Transparent Proxy Set Correctly = {is_transparent_proxy_set_correctly}')

    # Setting the 'Using different timezone' key's value pair to True
    checklist_items_dict['Using a tor connection'] = is_transparent_proxy_set_correctly
    

def get_the_public_ip_address():
    """A function which tries to displays the user's public ip address with notifications"""

    # Waiting for 1.5 seconds
    sleep(1.5)

    # Sending notification to let the user know that the application is trying to connect to the server
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Trying to connect to the server"')

    # Waiting for 1.5 seconds
    sleep(1.5)

    # Trying to execute the code block that is located inside this block
    try:
        # Sending a get request to "https://ifconfig.io" to get the public ip address.
        public_ip_address = run(["sudo", "-S", "bash", "-c", "curl --connect-timeout 7.5 {}".format("https://ifconfig.io")], input=user_pwd, text=True, capture_output=True).stdout.strip()

        # Creating a pattern for ip address validation
        ip_addr_regex = compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')
        
        # Checking if the get request's response is an ip address
        result = ip_addr_regex.search(public_ip_address).group()

        # Checking if pattern validation's result is equal to the get request's response
        if result == public_ip_address:

            # Creating a message that contain's the public ip address
            message = f'Your public ip address is {public_ip_address}'

        # Checking if the pattern validation's result is not equal to the get request's response
        else:
            
            # Creating a message that says "Couldn't connect to the server!"
            message = "Couldn't connect to the server!"

    # Instructing the computer about what to do if the application fails to send execute the code which is inside the try block
    except:

        # Creating a message that informs the user that it can't connect to the internet
        message = "Couldn't connect to the server!"

    # Sending notification
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "{message}"')


def manage_netfilter_service():
    """A function which starts and enables netfilter service if it's not"""

    netfilter_persistent_status = run(["sudo", "-S", "bash", "-c", "systemctl status netfilter-persistent"], input=user_pwd, text=True, capture_output=True).stdout.strip()

    # Checking if the netfilter-persistent service is inactive
    if 'inactive' in netfilter_persistent_status:

        # Starting the netfilter-persistent service
        run(["sudo", "-S", "bash", "-c", "systemctl start netfilter-persistent"], input=user_pwd, text=True, capture_output=True)

    # Checking if the netfilter-persistent service is disabled
    if 'disabled' in netfilter_persistent_status:

        # Enabling the netfilter service
        run(["sudo", "-S", "bash", "-c", "systemctl enable netfilter-persistent"], input=user_pwd, text=True, capture_output=True)


def kill_log_files():
    """A function which overrides the log files in the system"""
    
    # Sending a notification to inform the user that the operation is starting
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Shreading the log files"')

    # Waiting for 0.3 seconds
    sleep(0.3)

    # Executing the mac_changer script.
    system(f'bash {log_shredder_file_path} {current_username}')

    # Sending a notification to inform the user that the operation is done
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Log shredding has been done"')


def change_the_mac_address():
    """A function which changes the mac address"""

    def mac_changer_button_question_dialog_processor(i):
        """A function which checks the user's answer for the mac changer question and instructs the computer about what to do based on that answer"""

        # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
        user_answer = i.text()

        # Checking if the user pressed to the yes button.
        if user_answer == "&Yes":
            
            # Getting the active internet adaptors name 
            internet_adaptor_name = popen("ip route show default | awk '/default/ {print $5}'").read().strip()

            # Executing the mac_changer script.
            run(["sudo", "-S", "bash", "-c", "{}".format(str(mac_changer_script_file_path))], input=user_pwd, text=True, capture_output=True)

            # Waiting for 4 seconds
            sleep(4)

            # Connecting to internet
            run(f'sudo nmcli d connect {internet_adaptor_name}', shell=True, input=user_pwd, text=True, capture_output=True, executable="/bin/bash")
            # run(["sudo", "-S", "bash", "-c", "nmcli d connect {internet_adaptor_name}"], input=user_pwd, text=True, capture_output=True)

            # Sending a notification to inform the user that the operation is done
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Mac address has been changed"')

        # Checking if the user pressed to the no button
        elif user_answer == "&No":
            
            # Executing the mac_changer script.
            run(["sudo", "-S", "bash", "-c", "{}".format(str(mac_changer_script_file_path))], input=user_pwd, text=True, capture_output=True)

            # Sending a notification to inform the user that the operation is done
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Mac address has been changed"')

        # Checking if the didn't pressed to bot yes and not buttons 
        else:

            # Printing "Operation canceled in debug mode"
            debug("Operation canceled")

    # Sending a notification to inform the user that the operation is starting
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Changing the mac address"')
    
    # Waiting for 0.3 seconds
    sleep(0.3)

    # Creating a question dialog window
    question_dialog = QMessageBox()

    # Setting the question dialog window's icon
    question_dialog.setIcon(QMessageBox.Question)

    # Setting the dialog's window title
    question_dialog.setWindowTitle("Important")

    # Setting the question dialog's text
    question_dialog.setText("Do you want to connect back to the internet?")

    # Setting standard buttons
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

    # Adding functionality to Yes and No buttons
    question_dialog.buttonClicked.connect(mac_changer_button_question_dialog_processor)

    # Showing the question dialog
    question_dialog.exec_()


def wipe_the_memory():
    """A function which drops caches, wipes the memory securely and notifies the user"""

    def wipe_button_question_dialog_processor(i):
        """A function which process the input coming from the dialog box that is opened after the wipe button is pressed to identify what app should do"""
        
        # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
        user_answer = i.text()

        # Waiting for 0.3 seconds
        sleep(0.3)

        # Checking if the user pressed to the yes button.
        if user_answer == "&Yes":
            
            # Sending a notification to inform the user that the process is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Trying to wipe the memory and drop caches. This might take some time!"')

            # Executing the bomb.sh file to wipe the memory securely
            run(["sudo", "-S", "bash", "-c", "{}".format(fast_bomb_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Sending a notification to let the user know what the application just did
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Caches are dropped and memory is wiped"')
            
        # Checking if the user pressed to the no button
        elif user_answer == "&No":

            # Sending a notification to inform the user that the process is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Trying to wipe the memory and drop caches. This might take some time!"')

            # Executing the bomb.sh file to wipe the memory securely
            run(["sudo", "-S", "bash", "-c", "{}".format(secure_bomb_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Sending a notification to let the user know what the application just did
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Caches are dropped and memory is wiped"')

        # Checking if the didn't pressed to bot yes and not buttons 
        else:

            # Printing "Operation canceled in debug mode"
            debug("Operation canceled")

    # Creating a question dialog window
    question_dialog = QMessageBox()

    # Setting the question dialog window's icon
    question_dialog.setIcon(QMessageBox.Question)

    # Setting the dialog's window title
    question_dialog.setWindowTitle("Important")

    # Setting the question dialog's text
    question_dialog.setText("Do you want fast and less secure operation?")

    # Setting standard buttons
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

    # Adding functionality to Yes and No buttons
    question_dialog.buttonClicked.connect(wipe_button_question_dialog_processor)

    # Showing the question dialog
    question_dialog.exec_()
    

def reset_ghostsurf_settings():
    """A function which resets the ghostsurf settings"""

    def reset_button_question_dialog_processor(i):
        """A function which process the input coming from the dialog box that is opened after the reset button is pressed to identify what app should do"""
        
        # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
        user_answer = i.text()

        # Waiting for 0.3 seconds
        sleep(0.3)

        # Checking if the user pressed to the yes button.
        if user_answer == "&Yes":
            
            # Sending a notification to inform the user that the operation is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Resetting iptables rules only"')

            # Waiting for 0.3 seconds
            sleep(0.3)

            # Executing the reset.sh script.
            run(["sudo", "-S", "bash", "-c", "{}".format(reset_iptables_only_script_file_path)], input=user_pwd, text=True, capture_output=True)
            
            # Sending a notification to inform the user that the operation is done
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Iptables rules are reset"')
            
        # Checking if the user pressed to the no button
        elif user_answer == "&No":

            # Sending a notification to inform the user that the operation is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Resetting ghostsurf configurations"')

            # Waiting for 0.3 seconds
            sleep(0.3)

            # Executing the reset.sh script.
            run(["sudo", "-S", "bash", "-c", "{}".format(reset_script_file_path)], input=user_pwd, text=True, capture_output=True)
            
            # Sending a notification to inform the user that the operation is done
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Reseting is done"')

        # Checking if the didn't pressed to bot yes and not buttons 
        else:

            # Printing "Operation canceled in debug mode"
            debug("Operation canceled")

    # Creating a question dialog window
    question_dialog = QMessageBox()

    # Setting the question dialog window's icon
    question_dialog.setIcon(QMessageBox.Question)

    # Setting the dialog's window title
    question_dialog.setWindowTitle("Important")

    # Setting the question dialog's text
    question_dialog.setText("Do you want to reset iptables rules only?")

    # Setting standard buttons
    question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

    # Adding functionality to Yes and No buttons
    question_dialog.buttonClicked.connect(reset_button_question_dialog_processor)

    # Showing the question dialog
    question_dialog.exec_()


class WorkerSignals(QObject):
    """A worker signals class which defines the signals available from a running worker thread"""

    list_item = Signal(str)


class Worker(QRunnable):
    """A worker class which inherits from QRunnable to handle worker thread setup, signals and wrap-up"""

    def __init__(self):
        super().__init__()

        self.signals = WorkerSignals()

    # Creating a dictionary to store the checklist's keys and values
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
        
        # Calling the check_fake_hostname_usage function.
        check_fake_hostname_usage()

        # Calling the check_fake_mac_address_usage function.
        check_fake_mac_address_usage()

        # Calling the check_appropriate_nameserver_usage function.
        check_appropriate_nameserver_usage()

        # Calling the check_browser_anonymization function.
        check_browser_anonymization()

        # Calling the check_different_timezone_usage function.
        check_different_timezone_usage()

        # Calling the check_tor_connection_usage function.
        check_tor_connection_usage()

        # Iterating over each each key in cheklist dictionary's keys
        for key in checklist_items_dict.keys():
            
            # Emiting the key
            self.signals.list_item.emit(key)

            # Waiting for 0.02 seconds
            sleep(0.02)


class ChecklistModel(QAbstractListModel):
    """A data class called ChacklistModel to control how data objects will be created"""
    
    def __init__(self, list_items=None):

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


class ChecklistWindow(QWidget, Ui_ChecklistWindow):
    """A window class called ChecklistWindow created with QWidget subclass and Ui_ChecklistWindow user interface"""

    def __init__(self, *args, **kwargs):
        """An init function which makes the window self contained""" 

        # Calling super function with init
        super().__init__(*args, **kwargs)

        # Loading the GUI
        self.setupUi(self)

        # Creating a list model
        self.model = ChecklistModel()

        # Creating the thread pool
        self.threadpool = QThreadPool()

        # Setting the checklist_list_view object's list model
        self.checklist_list_view.setModel(self.model)

        # Creating a worker
        worker = Worker()
        
        # Connecting a function with the worker's signal
        worker.signals.list_item.connect(self.run_all_the_checks)

        # Starting the worker
        self.threadpool.start(worker)

    def run_all_the_checks(self, key):
        """A function which calls all of the checking functions and adds the checklist items to the checklist"""

        # Access the list via the model.
        self.model.list_items.append((checklist_items_dict[key], key))

        # Trigger refresh.
        self.model.layoutChanged.emit()


class PasswordWindow(QWidget, Ui_PasswordWindow):
    """A window class called that is created with QWdiged subclass and Ui_PasswordWindow user interface"""

    def __init__(self, *args, **kwargs):
        """An init function which makes the window self contained""" 

        # Calling super function with init
        super().__init__(*args, **kwargs)

        # Loading the GUI
        self.setupUi(self)

        # Connecting the submit button with the get_user_pwd function in a way that the function will going to trigger with a press signal.
        self.submit_button.pressed.connect(self.get_user_pwd)

        # Connecting the visibility_button with the change_echo_mode function in a way that the function will going to trigger with a press signal.
        self.visibility_button.pressed.connect(self.change_echo_mode)

    def change_echo_mode(self):
        """A function which changes the echo mode to hide and display the password"""
        
        # Creating a variable called echo_mode which is equal to the password_line_edit wiget's echo mode
        echo_mode = self.password_line_edit.echoMode()

        # Checking if the echo mode of the password_line_edit widget is Password
        if echo_mode == QLineEdit.EchoMode.Password:

            # Changing the widget's echo mode to Normal
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)

            # Creating an icon
            open_eye_icon = QIcon()

            # Adding pixmap to the icon
            open_eye_icon.addPixmap(QPixmap(str(Path(base_dir, "icons", "eye_open.svg"))))

            # Setting the eye_button's icon
            self.visibility_button.setIcon(open_eye_icon)

        # Checking if the echo mode of the password_line_edit widget is not Password
        else:

            # Changing the widget's echo mode to Password
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

            # Creating an icon
            closed_eye_icon = QIcon()

            # Adding pixmap to the icon
            closed_eye_icon.addPixmap(QPixmap(str(Path(base_dir, "icons", "eye_closed.svg"))))

            # Setting the eye_button's icon
            self.visibility_button.setIcon(closed_eye_icon)

    def get_user_pwd(self):
        """A function which stores the password that the user entered in a global variable"""
        
        # Creating a global variable called user_pwd
        global user_pwd

        # Initializing the user_pwd variable with the password_line_edit's text
        user_pwd = self.password_line_edit.text()

        # Getting the username and the root privileges
        user_name = run(["sudo", "-S", "whoami"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        # Checking if the username is equal to root
        if user_name == "root":

            # Closing password window
            self.close()

            # Creating a main_window object from MainWindow class with a global scope
            global main_window
            main_window = MainWindow()

            # Showing the main window
            main_window.show()

        # Checking if the username is not equal to root
        else:

            # Creating a warning dialog window
            warning_dialog = QMessageBox()

            # Setting the warning dialog window's icon
            warning_dialog.setIcon(QMessageBox.Critical)

            # Setting the dialog's window title
            warning_dialog.setWindowTitle("Warning")

            # Setting the warning dialog's text
            warning_dialog.setText("Couldn't get root privileges!")

            # Showing the warning dialog
            warning_dialog.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    """A MainWindow class created with QMainWindow subclass and Ui_MainWindow user interface"""

    def __init__(self, *args, **kwargs):
        """An init function which makes the window self contained""" 
        
        # Calling super function with init
        super().__init__(*args, **kwargs)

        # Loading the GUI
        self.setupUi(self)

        # Calling the manage_netfilter_service function.
        manage_netfilter_service()

        # Checking tor services status
        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()
        
        # Opening the ghostsurf.conf file in reading mode
        with open(ghostsurf_configuration_file_path, "r") as ghostsurf_configuraion_file:
            
            # Reading the lines of ghostsurf.conf file
            ghostsurf_configuraion_file_contents = ghostsurf_configuraion_file.readlines()

            # Checking if "enabled_at_boot=yes" is in the line
            if "enabled_at_boot=yes\n" in ghostsurf_configuraion_file_contents:

                # Creating a variable to keep track if ghostsurf is enabled at boot
                is_ghostsurf_enabled_at_boot = True

            # Checking if "enabled_at_boot=no" is not in the line
            else:

                # Creating a variable to keep track if ghostsurf is enabled at boot
                is_ghostsurf_enabled_at_boot = False

        # Checking if is_ghostsurf_enabled_at_boot is equal to True
        if is_ghostsurf_enabled_at_boot == True: 

            # Changing the start_stop_button's text value to "Stop".
            self.start_stop_button.setText("Stop")

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: green;}")

            # Setting the status_label's text to "Active"
            self.status_label.setText('Active')
            
            # Changing the ultra_ghost_button's text to "enabled"
            self.ultra_ghost_button.setText("enabled")

            # Setting the style sheet of the ultra_ghost_button 
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")

        # Checking if the tor service is inactive
        if "inactive" in tor_status:

            # Setting the status_label's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: red;}")

            # Setting the status_label's text to "inactive"
            self.status_label.setText('Inactive')

        # Checking if the tor service is active
        else:

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: green;}")

            # Setting the status_label's text to active
            self.status_label.setText('Active')
        
        # Connecting the start_stop_button with the start_stop function in a way that the function will going to trigger with a press signal
        self.start_stop_button.pressed.connect(self.start_stop)

        # Connecting the my_ip_button with the show_my_ip function in a way that the function will going to trigger with a press signal
        self.my_ip_button.pressed.connect(self.show_my_ip)

        # Connecting the status_button with the show_status function in a way that the function will going to trigger with a press signal
        self.status_button.pressed.connect(self.show_status)

        # Connecting the change_ip_button with the change_id function in a way that the function will going to trigger with a press signal
        self.change_ip_button.pressed.connect(self.change_id)

        # Connecting the info_button with the open_info_page function in a way that the function will going to trigger with a press signal
        self.info_button.pressed.connect(self.open_info_page) 

        # Connecting the pandora_bomb_button with the wipe_memory_securely function in a way that the function will going to trigger with a press signal
        self.pandora_bomb_button.pressed.connect(self.wipe_memory_securely)

        # Connecting the ultra_ghost_button with the ultra_ghost_mode function in a way that the function will going to trigger with a press signal
        self.ultra_ghost_button.pressed.connect(self.ultra_ghost_mode)

        # Connecting the mac_changer_button with the change_mac_address function in a way that the function will going to trigger with a press signal
        self.mac_changer_button.pressed.connect(self.change_mac_address)

        # Connecting the log_shredder_button with the shred_log_files function in a way that the function will going to trigger with a press signal
        self.log_shredder_button.pressed.connect(self.shred_log_files)

        # Connecting the reset_button with the reset_settings function in a way that the function will going to trigger with a press signal
        self.reset_button.pressed.connect(self.reset_settings)

        # Connecting the dns_changer_button with the change_dns function in a way that the function will going to trigger with a press signal
        self.dns_changer_button.pressed.connect(self.change_dns)

        # Connecting the hostname_changer_button with the change_hostname function in a way that the function will going to trigger with a press signal
        self.hostname_changer_button.pressed.connect(self.change_hostname)

        # Connecting the run_fast_check_button with the display_checklist function in a way that the function will going to trigger with a press signal
        self.run_fast_check_button.pressed.connect(self.run_fast_check)

        # Connecting the browser_anonymizer_button with the anonymize_the_browser function in way that the function will going to trigger with a press signal
        self.browser_anonymizer_button.pressed.connect(self.anonymize_the_browser)

    def anonymize_the_browser(self):
        """A function which anonymizes firefox by changing it's preferences"""

        # Sending a notification to let the user know what happening
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Creating Ghostsurf\'s Firefox profiles"')

        # Waiting for 0.3 seconds
        sleep(0.3)

        # Create a firefox profile called ghostsurf
        run(["firefox-esr", "-CreateProfile", "ghostsurf"], text=True, capture_output=True)

        # Create a firefox profile called penetration testing
        run(["firefox-esr", "-CreateProfile", "penetration-testing"], text=True, capture_output=True)

        # Checking if the path that leads to custom preferences file is exists
        if custom_firefox_preferences_file_path.exists() == True:
        
            # Opening the custom preferences file in read mode
            with open(custom_firefox_preferences_file_path, "r") as the_custom_prefs_file:

                # Creating a list of lines by reading the file
                custom_prefs = the_custom_prefs_file.read()

        # Checking if the path is not exists
        else:

            # Sending a notification to inform the user that the operation is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Custom preferences file not found. Try to reinstall ghostsurf!"')

        ghostsurf_firefox_profile_file_path = Path(run(["bash", "-c", "find /home/{}/.mozilla/firefox/ -name *.ghostsurf".format(current_username)], text=True, capture_output=True).stdout.strip(), "user.js")

        with open(ghostsurf_firefox_profile_file_path, "w") as ghostsurf_firefox_profile_user_pref_file:

            ghostsurf_firefox_profile_user_pref_file.write(custom_prefs)

        # Executing the init script.
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

        # Sending a notification to inform the user that the firefox preferences has been set
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Ghostsurf\'s Firefox profiles are created. And, preferences are set."')

    def run_fast_check(self):
        """A function which runs a fast check and displays the checklist in a window"""

        # Printing the operation's summary in debug mode        
        debug("Running a fast check")

        # Creating an object from the dialog class
        self.checklist_window = ChecklistWindow()

        # Executing the object to display the window.
        self.checklist_window.show()

    def change_hostname(self):
        """A function which changes the hostname. Note: Modems sees your hostname not your username"""

        # Creating a question dialog window
        question_dialog = QMessageBox()

        # Setting the question dialog window's icon
        question_dialog.setIcon(QMessageBox.Question)

        # Setting the dialog's window title
        question_dialog.setWindowTitle("Important")

        # Setting the question dialog's text
        question_dialog.setText("This operation requires reboot. Do you allow to reboot this system?")

        # Setting standard buttons
        question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

        # Showing the question dialog
        question_dialog_answer = question_dialog.exec_()

        # Checking if the user pressed to the yes button.
        if question_dialog_answer == QMessageBox.Yes:

            # Priting what's going on in debug mode
            debug("Rebooting the system")

            # Executing the stop script
            run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Executing the hostname_changer script
            run(["sudo", "-S", "bash", "-c", "{}".format(hostname_changer_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Rebooting the system
            run(["sudo", "reboot"], input=user_pwd, text=True, capture_output=True)

        # Checking if user didn't pressed to the yes button
        else:

            # Printing "Operation canceled" in debug mode
            debug("Operation canceled")

    def change_dns(self):
        """A function which changes the nameservers in the resolv.conf file"""

        # Sending a notification to inform the user that the operation is starting
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Changing the nameservers"')

        # Waiting for 0.3 seconds
        sleep(0.3)

        # Getting the working status of the application from the start_stop_button's text
        working_status = self.start_stop_button.text()

        # Checking if transparent proxy is on
        if working_status == "Stop":
            
            # Executing the nameservers_changer script
            run(["sudo", "-S", "bash", "-c", f'{nameserver_changer_file_path} {tor_nameservers_file_path}'], input=user_pwd, text=True, capture_output=True)

            # Copying and pasting custom nameservers for tor on resolv.conf file
            run(["sudo", "-S", "bash", "-c", f'cp {tor_nameservers_file_path} {original_resolv_configuration_file_path}'], input=user_pwd, text=True, capture_output=True)

        # Checking if transparent proxy is off
        else:

            # Executing the nameservers_changer script
            run(["sudo", "-S", "bash", "-c", f'{nameserver_changer_file_path} {privacy_focused_nameservers_file_path}'], input=user_pwd, text=True, capture_output=True)

            # Copying and pasting dns_changer nameservers to on resolv.conf file
            run(["sudo", "-S", "bash", "-c", f'cp {privacy_focused_nameservers_file_path} {original_resolv_configuration_file_path}'], input=user_pwd, text=True, capture_output=True)            

        # Sending a notification to inform the user that the operation is done
        system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Nameservers has been changed"')

    def reset_settings(self):
        """A function which resets ghostsurf settings"""

        # Creating a thread that resets the ghostsurf settings
        reset_thread = Thread(target=reset_ghostsurf_settings)

        # Starting the thread
        reset_thread.start()

    def shred_log_files(self):
        """A function which shreds the log files"""

        # Creating a thread that kills the log files
        log_kill_thread = Thread(target=kill_log_files)

        # Starting the thread
        log_kill_thread.start()

    def change_mac_address(self):
        """A function which changes the mac address"""
        
        # Creating a thread that changes the mac address
        mac_changer_thread = Thread(target=change_the_mac_address)

        # Starting the thread
        mac_changer_thread.start()

    def ultra_ghost_mode(self):
        """A function which enables/disables ghostsurf at boot"""

        # Getting the ultra ghost mode's status from the button's text
        ultra_ghost_mode_status = self.ultra_ghost_button.text()

        # Checking if ultra_ghost_mode_status is equal to "disabled"
        if ultra_ghost_mode_status == "disabled":

            # Printing what's going on in debug mode
            debug("Enabling ghostsurf at boot")

            # Executing the start script
            run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Executing the save script
            run(["sudo", "-S", "bash", "-c", "{}".format(save_iptables_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Opening the ghostsurf.conf file in read mode
            with open(ghostsurf_configuration_file_path, "r") as a:

                # Reading the lines of the ghostsurf.conf file
                a_contents = a.readlines()
                    
                # Checking if "enabled_at_boot=no\n"" is in the list of lines
                if "enabled_at_boot=no\n" in a_contents:
                    
                    # Finding the index number of "enabled_at_boot=no\n" string
                    line_index = a_contents.index("enabled_at_boot=no\n")

                    # Updating the a_contents list
                    a_contents[line_index]="enabled_at_boot=yes\n"

                    # Printing list of ghostsurf configuration file lines in debug mode 
                    debug(a_contents)

            # Opening the ghostsurf.conf file in write mode
            with open(ghostsurf_configuration_file_path, "w") as b:

                # Writing the new contents to file
                b.write(''.join(a_contents))

            # Changing the start_stop_button's text value to "Stop".
            self.start_stop_button.setText("Stop")

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: green;}")

            # Setting the status_label's text to "Active"
            self.status_label.setText('Active')
            
            # Changing the ultra_ghost_button's text to "enabled"
            self.ultra_ghost_button.setText("enabled")

            # Setting the style sheet of the ultra_ghost_button 
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: #00ff00; border-radius: 4px; border: 1px solid black}")

        # Checking if ultra_ghost_mode_status is not equal to "disabled"
        else:

            # Printing what's going on in debug mode
            debug("Disabling ghostsurf at boot")

            # Executing the stop script
            run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

            # Opening the ghostsurf.conf file in read mode
            with open(ghostsurf_configuration_file_path, "r") as a:
                
                # Reading the lines of ghostsurf.conf file and creating a list out of them
                a_contents = a.readlines()

                # Checking if "enabled_at_boot=enabled" is in the line
                if "enabled_at_boot=yes\n" in a_contents:
                    
                    # Finding the index of the line
                    line_index = a_contents.index("enabled_at_boot=yes\n")

                    # Changing the line corresponding to the index number
                    a_contents[line_index]="enabled_at_boot=no\n"

            # Opening the ghostsurf.conf file in write mode
            with open(ghostsurf_configuration_file_path, "w") as b:
                
                # Writing the new contents in to file
                b.write(''.join(a_contents))

            # Changing the start_stop_button's text value to "Start".
            self.start_stop_button.setText("Start")

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: red;}")

            # Setting the status_label's text to "Inactive"
            self.status_label.setText('Inactive')
            
            # Changing the ultra_ghost_button's text to "disabled"
            self.ultra_ghost_button.setText("disabled")

            # Setting the style sheet of the ultra_ghost_button 
            self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")  

    def wipe_memory_securely(self):
        """A function which wipes the memory securely"""

        # Creating a thread that targerts the wipe_the_memory function
        wipe_memory_thread = Thread(target=wipe_the_memory)

        # Starting the thread
        wipe_memory_thread.start()

    def open_info_page(self):
        """A function which opens the info page in the default browser"""

        # Opening the info page of this application in the default browser
        wbopen(help_page_url)

    def start_stop(self):
        """A function which redirects all internet traffic over tor"""

        def start_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the start button is pressed to identify what app should do"""

            # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
            user_answer = i.text()

            # Checking if the user pressed to the yes button.
            if user_answer == "&Yes":

                # Printing the name of the button that is clicked in debug mode
                debug("Yes button is clicked")

                # Executing the init script.
                run(["sudo", "-S", "bash", "-c", "{}".format(init_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Executing the start script
                run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Changing the start_stop_button's text value to Stop.
                self.start_stop_button.setText("Stop")

            # Checking if the user pressed to the no button
            elif user_answer == "&No":

                # Printing the name of the button that is clicked in debug mode
                debug("No button is clicked")
                
                # Executing the start script
                run(["sudo", "-S", "bash", "-c", "{}".format(start_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Changing the start_stop_button's text value to Stop.
                self.start_stop_button.setText("Stop")

            # Checking if the didn't pressed to bot yes and not buttons 
            else:

                # Printing "Operation canceled in debug mode"
                debug("Operation canceled")

        def stop_button_question_dialog_processor(i):
            """A function which process the input coming from the dialog box that is opened after the stop button is pressed to identify what app should do"""

            # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
            user_answer = i.text()

            # Checking if the user pressed to the yes button.
            if user_answer == "&Yes":

                # Executing the init script.
                run(["sudo", "-S", "bash", "-c", "{}".format(init_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Executing the stop script.
                run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Opening the ghostsurf.conf file in read mode
                with open(ghostsurf_configuration_file_path, "r") as d:

                    # Reading the lines of the file
                    d_contents = d.readlines()

                    # Checking if "enabled_at_boot=yes\n" in the list of lines
                    if "enabled_at_boot=yes\n" in d_contents:
                        
                        # Finding the index number of the line corresponding to the string
                        line_index = d_contents.index("enabled_at_boot=yes\n")

                        # Modiftying the list item corresponding to the index number
                        d_contents[line_index] = "enabled_at_boot=no\n"

                # Opening the ghostsurf.conf file in write mode
                with open(ghostsurf_configuration_file_path, "w") as e:

                    # Writing the new contents into file
                    e.write("\n".join(d_contents))

                # Changing the start_stop_button's text value to Stop.
                self.start_stop_button.setText("Start")

                # Changing the ultra_ghost_button's text to "disabled"
                self.ultra_ghost_button.setText("disabled")

                # Setting the style sheet of the ultra_ghost_button 
                self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")

            # Checking if the user pressed to the no button
            elif user_answer == "&No":

                # Executing the stop script.
                run(["sudo", "-S", "bash", "-c", "{}".format(stop_transparent_proxy_script_file_path)], input=user_pwd, text=True, capture_output=True)

                # Opening the ghostsurf.conf file in read mode
                with open(ghostsurf_configuration_file_path, "r") as d:

                    # Reading the lines of the file
                    d_contents = d.readlines()

                    # Checking if "enabled_at_boot=yes\n" in the list of lines
                    if "enabled_at_boot=yes\n" in d_contents:
                        
                        # Finding the index number of the line corresponding to the string
                        line_index = d_contents.index("enabled_at_boot=yes\n")

                        # Modiftying the list item corresponding to the index number
                        d_contents[line_index] = "enabled_at_boot=no\n"

                # Opening the ghostsurf.conf file in write mode
                with open(ghostsurf_configuration_file_path, "w") as e:

                    # Writing the new contents into file
                    e.write("\n".join(d_contents))

                # Changing the start_stop_button's text value to Stop.
                self.start_stop_button.setText("Start")

                # Changing the ultra_ghost_button's text to "disabled"
                self.ultra_ghost_button.setText("disabled")

                # Setting the style sheet of the ultra_ghost_button 
                self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {background: red; border-radius: 4px; border: 1px solid black}")

            # Checking if the didn't pressed to bot yes and not buttons 
            else:

                # Printing "Operation canceled in debug mode"
                debug("Operation canceled")
        
        # Checking if the start_stop_button's text is equal to "Start"
        if self.start_stop_button.text() == "Start":

            # Printing "Start button pressed" in debug mode.
            debug("Start button pressed")

            # Creating a question dialog window
            question_dialog = QMessageBox()

            # Setting the question dialog window's icon
            question_dialog.setIcon(QMessageBox.Question)

            # Setting the dialog's window title
            question_dialog.setWindowTitle("Important")

            # Setting the question dialog's text
            question_dialog.setText("Are you allowing to killing of dangerous applications and cleaning of dangerous caches?")

            # Setting standard buttons
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

            # Adding functionality to Yes and No buttons
            question_dialog.buttonClicked.connect(start_button_question_dialog_processor)

            # Showing the question dialog
            question_dialog.exec_()
            
        # Checking if the start_stop_button's text is not equal to "Start"
        else:

            # Printing "Stop button pressed" in debug mode
            debug("Stop button pressed")

            # Creating a question dialog window
            question_dialog = QMessageBox()

            # Setting the question dialog window's icon
            question_dialog.setIcon(QMessageBox.Question)

            # Setting the dialog's window title
            question_dialog.setWindowTitle("Important")

            # Setting the question dialog's text
            question_dialog.setText("Are you allowing to killing of dangerous applications and cleaning of dangerous caches?")

            # Setting standard buttons
            question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

            # Adding functionality to Yes and No buttons
            question_dialog.buttonClicked.connect(stop_button_question_dialog_processor)

            # Showing the question dialog
            question_dialog.exec_() 

        # Reading the tor service's status by running a system command.
        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        # Checking if tor service is inactive
        if "inactive" in tor_status:

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: red;}")

            # Setting the status_label's text to "Inactive"
            self.status_label.setText('Inactive')

        # Checking if tor service is active
        else:

            # Setting the status_label widget's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: green;}")

            # Setting the status_label's text to "Active"
            self.status_label.setText('Active')

    def show_my_ip(self):
        """A function which shows your public ip address"""
        
        # Creating a thread start uses the get_the_public_ip_address function 
        public_ip_thread = Thread(target=get_the_public_ip_address)

        # Starting the thread
        public_ip_thread.start()

    def show_status(self):
        """A function which shows the tor service's status"""

        # Reading tor services status from a system command
        tor_status = run(["sudo", "-S", "bash", "-c", "systemctl status tor.service"], input=user_pwd, text=True, capture_output=True).stdout.strip()

        # Checking if tor service is inactive
        if "inactive" in tor_status:

            # Setting the status_label's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: red;}")

            # Setting the status_label's text to "Inactive"
            self.status_label.setText('Inactive')
        
        # Checking if tor service is active
        else:

            # Setting the status_label's stylesheet
            self.status_label.setStyleSheet(u"#status_label {color: green;}")

            # Setting the status_label's text to "Active"
            self.status_label.setText('Active')

    def change_id(self):
        """A function which changes your ip address by restarting the transparent proxy"""

        # Restarting the tor service to change the ip address.
        run(["sudo", "-S", "bash", "-c", "systemctl restart tor"], input=user_pwd, text=True, capture_output=True)


# Evaluate if the source is being run on its own or being imported somewhere else. With this conditional in place, your code can not be imported somewhere else.
if __name__ == "__main__":

    # Calling the main function
    main()
