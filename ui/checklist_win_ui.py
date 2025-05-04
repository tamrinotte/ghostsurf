# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checklist_win.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QListView, QSizePolicy, QWidget)
import resources_rc

class Ui_ChecklistWindow(object):
    def setupUi(self, ChecklistWindow):
        if not ChecklistWindow.objectName():
            ChecklistWindow.setObjectName(u"ChecklistWindow")
        ChecklistWindow.resize(290, 270)
        ChecklistWindow.setMinimumSize(QSize(290, 270))
        ChecklistWindow.setMaximumSize(QSize(290, 270))
        icon = QIcon()
        icon.addFile(u":/logos/ghostsurf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        font.setFamilies([u"Ubuntu"])
        font.setBold(False)
        font.setItalic(False)
        self.checklist_list_view.setFont(font)

        self.retranslateUi(ChecklistWindow)

        QMetaObject.connectSlotsByName(ChecklistWindow)
    # setupUi

    def retranslateUi(self, ChecklistWindow):
        ChecklistWindow.setWindowTitle(QCoreApplication.translate("ChecklistWindow", u"Anonymity Checklist", None))
    # retranslateUi

