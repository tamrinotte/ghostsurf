# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
from PySide6.QtWidgets import QMessageBox

# Ghostsurf Modules
from modules.conf_logging import error

##############################

# QUESTION DIALOGS

##############################

def show_question_dialog(title, text, on_click_handler):
    try:
        question_dialog = QMessageBox()
        question_dialog.setIcon(QMessageBox.Question)
        question_dialog.setWindowTitle(title)
        question_dialog.setText(text)
        question_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        question_dialog.buttonClicked.connect(on_click_handler)
        question_dialog.exec_()
    except Exception as e:
        message = "Failed to show question dialog."
        error(f"{message} - {e}")

def ask_confirmation(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")