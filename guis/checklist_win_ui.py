# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checklist_win.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_ChecklistWindow(object):
    def setupUi(self, ChecklistWindow):
        if not ChecklistWindow.objectName():
            ChecklistWindow.setObjectName(u"ChecklistWindow")
        ChecklistWindow.resize(290, 270)
        ChecklistWindow.setMinimumSize(QSize(290, 270))
        ChecklistWindow.setMaximumSize(QSize(290, 270))
        icon = QIcon()
        icon.addFile(u":/logos/ghostsurf.png", QSize(), QIcon.Normal, QIcon.Off)
        ChecklistWindow.setWindowIcon(icon)
        ChecklistWindow.setStyleSheet(u"#ChecklistWindow {\n"
"	background: #231f1f;\n"
"}")
        self.checklist_list_view = QListView(ChecklistWindow)
        self.checklist_list_view.setObjectName(u"checklist_list_view")
        self.checklist_list_view.setGeometry(QRect(0, 0, 290, 270))
        self.checklist_list_view.setMinimumSize(QSize(0, 0))
        self.checklist_list_view.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(u"Ubuntu")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.checklist_list_view.setFont(font)

        self.retranslateUi(ChecklistWindow)

        QMetaObject.connectSlotsByName(ChecklistWindow)
    # setupUi

    def retranslateUi(self, ChecklistWindow):
        ChecklistWindow.setWindowTitle(QCoreApplication.translate("ChecklistWindow", u"Anonymity Checklist", None))
    # retranslateUi

