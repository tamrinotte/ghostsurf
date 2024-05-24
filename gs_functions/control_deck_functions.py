# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from time import sleep
from os import system, popen
from subprocess import run
from re import compile
from threading import Thread
from logging import basicConfig, DEBUG, debug, disable, CRITICAL

# PySide2
from PySide2.QtWidgets import QMessageBox



# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
# disable(CRITICAL)



##############################

# SUB FUNCTIONS

##############################

def less_secure_memory_wipe(user_pwd, fast_bomb_script_file_path):
    """A function which runs a fast memory wipe"""

    # Executing the bomb.sh file to wipe the memory securely
    run(["sudo", "-S", "bash", "-c", "{}".format(fast_bomb_script_file_path)], input=user_pwd, text=True, capture_output=True)

    # Sending a notification to let the user know what the application just did
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Caches are dropped and memory is wiped"')

def secure_memory_wipe(user_pwd, secure_bomb_script_file_path):
    """A function which runs a secure memory wipe"""

    # Executing the bomb.sh file to wipe the memory securely
    run(["sudo", "-S", "bash", "-c", "{}".format(secure_bomb_script_file_path)], input=user_pwd, text=True, capture_output=True)

    # Sending a notification to let the user know what the application just did
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Caches are dropped and memory is wiped"')

def change_the_mac_address_and_connect_back_to_wifi(user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path):
    """A function which changes the computer's mac address and connects back to the internet"""

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

def change_ns(user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path):
    """A function which changes the name servers"""

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



##############################

# CONTROL DECK(MAIN) FUNCTIONS

##############################

def get_the_public_ip_address(user_pwd, ghostsurf_logo_file_path):
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

def kill_log_files(ghostsurf_logo_file_path, log_shredder_file_path, current_username):
    """A function which overrides the log files in the system"""
    
    # Sending a notification to inform the user that the operation is starting
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Shreading the log files"')

    # Waiting for 0.3 seconds
    sleep(0.3)

    # Executing the mac_changer script.
    system(f'bash {log_shredder_file_path} {current_username}')

    # Sending a notification to inform the user that the operation is done
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Log shredding has been done"')

def reset_ghostsurf_settings(user_pwd, ghostsurf_logo_file_path, reset_iptables_only_script_file_path, reset_script_file_path):
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

def change_the_mac_address(user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path):
    """A function which changes the mac address"""

    def mac_changer_button_question_dialog_processor(i):
        """A function which checks the user's answer for the mac changer question and instructs the computer about what to do based on that answer"""

        # Getting the user's answer from the i's text value to identify if the user pressed to yes or no
        user_answer = i.text()

        # Checking if the user pressed to the yes button.
        if user_answer == "&Yes":
            
            mac_changer_thread = Thread(target=change_the_mac_address_and_connect_back_to_wifi, args=[user_pwd, ghostsurf_logo_file_path, mac_changer_script_file_path])

            mac_changer_thread.start()

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

def wipe_the_memory(user_pwd, ghostsurf_logo_file_path, fast_bomb_script_file_path, secure_bomb_script_file_path):
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
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Wiping the memory and droping caches. This might take some time!"')

            # Creating a thread that targerts the wipe_the_memory function
            wipe_memory_thread = Thread(target=less_secure_memory_wipe, args=[user_pwd, fast_bomb_script_file_path])

            # Starting the thread
            wipe_memory_thread.start()

        # Checking if the user pressed to the no button
        elif user_answer == "&No":

            # Sending a notification to inform the user that the process is starting
            system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Wiping the memory and droping caches. This might take some time!"')

            # Creating a thread that targerts the wipe_the_memory function
            wipe_memory_thread = Thread(target=less_secure_memory_wipe, args=[user_pwd, secure_bomb_script_file_path])

            # Starting the thread
            wipe_memory_thread.start()

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

def change_the_nameservers(user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path):
    """A function which changes the nameservers to enhance security and privacy"""

    # Sending a notification to inform the user that the operation is starting
    system(f'notify-send -i "{ghostsurf_logo_file_path}" -t 150 "Changing the nameservers"')

    # Waiting for 0.3 seconds
    sleep(0.3)

    change_the_ns = Thread(target=change_ns, args=[user_pwd, ghostsurf_logo_file_path, working_status, nameserver_changer_file_path, tor_nameservers_file_path, original_resolv_configuration_file_path, privacy_focused_nameservers_file_path])

    change_the_ns.start()