# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'password_win.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)
import resources_rc

class Ui_PasswordWindow(object):
    def setupUi(self, PasswordWindow):
        if not PasswordWindow.objectName():
            PasswordWindow.setObjectName(u"PasswordWindow")
        PasswordWindow.resize(250, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PasswordWindow.sizePolicy().hasHeightForWidth())
        PasswordWindow.setSizePolicy(sizePolicy)
        PasswordWindow.setMinimumSize(QSize(250, 200))
        PasswordWindow.setMaximumSize(QSize(250, 200))
        icon = QIcon()
        icon.addFile(u":/logos/ghostsurf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PasswordWindow.setWindowIcon(icon)
        PasswordWindow.setStyleSheet(u"#PasswordWindow {\n"
"	background: #231f1f;\n"
"}")
        self.password_line_edit = QLineEdit(PasswordWindow)
        self.password_line_edit.setObjectName(u"password_line_edit")
        self.password_line_edit.setGeometry(QRect(50, 100, 150, 30))
        self.password_line_edit.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.setAlignment(Qt.AlignCenter)
        self.visibility_button = QPushButton(PasswordWindow)
        self.visibility_button.setObjectName(u"visibility_button")
        self.visibility_button.setGeometry(QRect(210, 108, 15, 15))
        self.visibility_button.setStyleSheet(u"#visibility_button {\n"
"	background: #231f1f;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/eye_closed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/eye_open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.visibility_button.setIcon(icon1)
        self.submit_button = QPushButton(PasswordWindow)
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setGeometry(QRect(80, 145, 90, 25))
        self.description_text = QLabel(PasswordWindow)
        self.description_text.setObjectName(u"description_text")
        self.description_text.setGeometry(QRect(20, 20, 210, 70))
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.description_text.setFont(font)
        self.description_text.setStyleSheet(u"#description_text {\n"
"	color: white;\n"
"}")
        self.description_text.setAlignment(Qt.AlignCenter)
        self.description_text.setWordWrap(True)

        self.retranslateUi(PasswordWindow)

        QMetaObject.connectSlotsByName(PasswordWindow)
    # setupUi

    def retranslateUi(self, PasswordWindow):
        PasswordWindow.setWindowTitle(QCoreApplication.translate("PasswordWindow", u"Password", None))
        self.password_line_edit.setText("")
        self.password_line_edit.setPlaceholderText(QCoreApplication.translate("PasswordWindow", u"User Password...", None))
        self.visibility_button.setText("")
        self.submit_button.setText(QCoreApplication.translate("PasswordWindow", u"Submit", None))
        self.description_text.setText(QCoreApplication.translate("PasswordWindow", u"Enter the password to get the root privileges", None))
    # retranslateUi

