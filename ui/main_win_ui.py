# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_win.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(330, 290)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(330, 290))
        MainWindow.setMaximumSize(QSize(330, 290))
        font = QFont()
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/logos/ghostsurf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(330, 290))
        self.centralwidget.setMaximumSize(QSize(330, 290))
        self.centralwidget.setStyleSheet(u"#centralwidget {\n"
"	background: #231f1f;\n"
"}")
        self.logo_label = QLabel(self.centralwidget)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setGeometry(QRect(0, 0, 100, 100))
        self.logo_label.setPixmap(QPixmap(u":/logos/ghostsurf.png"))
        self.logo_label.setScaledContents(True)
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(99, 9, 221, 71))
        font1 = QFont()
        font1.setFamilies([u"URW Bookman"])
        font1.setPointSize(30)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setStrikeOut(False)
        self.title_label.setFont(font1)
        self.title_label.setStyleSheet(u"#title_label {\n"
"	color: #6bfffb;\n"
"}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.start_stop_button = QPushButton(self.centralwidget)
        self.start_stop_button.setObjectName(u"start_stop_button")
        self.start_stop_button.setGeometry(QRect(20, 240, 90, 30))
        font2 = QFont()
        font2.setFamilies([u"Ubuntu"])
        font2.setStrikeOut(False)
        self.start_stop_button.setFont(font2)
        self.change_ip_button = QPushButton(self.centralwidget)
        self.change_ip_button.setObjectName(u"change_ip_button")
        self.change_ip_button.setGeometry(QRect(120, 240, 90, 30))
        self.my_ip_button = QPushButton(self.centralwidget)
        self.my_ip_button.setObjectName(u"my_ip_button")
        self.my_ip_button.setGeometry(QRect(220, 240, 90, 30))
        self.status_header_label = QLabel(self.centralwidget)
        self.status_header_label.setObjectName(u"status_header_label")
        self.status_header_label.setGeometry(QRect(160, 100, 80, 20))
        font3 = QFont()
        font3.setBold(True)
        font3.setUnderline(False)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.status_header_label.setFont(font3)
        self.status_header_label.setStyleSheet(u"#status_header_label {\n"
"	color: white;\n"
"}")
        self.status_header_label.setAlignment(Qt.AlignCenter)
        self.status_label = QLabel(self.centralwidget)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(240, 100, 70, 20))
        font4 = QFont()
        font4.setBold(True)
        font4.setUnderline(True)
        font4.setStrikeOut(False)
        font4.setKerning(True)
        self.status_label.setFont(font4)
        self.status_label.setStyleSheet(u"#status_label {\n"
"	color: red;\n"
"}")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.info_button = QPushButton(self.centralwidget)
        self.info_button.setObjectName(u"info_button")
        self.info_button.setGeometry(QRect(280, 180, 30, 30))
        self.info_button.setStyleSheet(u"#info_button {\n"
"	background: #231f1f;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/info.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.info_button.setIcon(icon1)
        self.pandora_bomb_button = QPushButton(self.centralwidget)
        self.pandora_bomb_button.setObjectName(u"pandora_bomb_button")
        self.pandora_bomb_button.setGeometry(QRect(280, 140, 30, 30))
        self.pandora_bomb_button.setStyleSheet(u"#pandora_bomb_button {\n"
"	background: #231f1f;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/bomb.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pandora_bomb_button.setIcon(icon2)
        self.ultra_ghost_button = QPushButton(self.centralwidget)
        self.ultra_ghost_button.setObjectName(u"ultra_ghost_button")
        self.ultra_ghost_button.setGeometry(QRect(10, 150, 80, 26))
        self.ultra_ghost_button.setStyleSheet(u"#ultra_ghost_button {\n"
"	background: red;\n"
"	border-radius: 4px;\n"
"	border: 1px solid black;\n"
"}")
        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setGeometry(QRect(240, 180, 30, 30))
        self.reset_button.setStyleSheet(u"#reset_button {\n"
"	background: #231f1f;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/reset.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.reset_button.setIcon(icon3)
        self.mac_changer_button = QPushButton(self.centralwidget)
        self.mac_changer_button.setObjectName(u"mac_changer_button")
        self.mac_changer_button.setGeometry(QRect(160, 140, 30, 30))
        self.mac_changer_button.setStyleSheet(u"#mac_changer_button {\n"
"	background: #231f1f;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/mac_changer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.mac_changer_button.setIcon(icon4)
        self.log_shredder_button = QPushButton(self.centralwidget)
        self.log_shredder_button.setObjectName(u"log_shredder_button")
        self.log_shredder_button.setGeometry(QRect(240, 140, 30, 30))
        self.log_shredder_button.setStyleSheet(u"#log_shredder_button {\n"
"	background: #231f1f;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/log_shredder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.log_shredder_button.setIcon(icon5)
        self.hostname_changer_button = QPushButton(self.centralwidget)
        self.hostname_changer_button.setObjectName(u"hostname_changer_button")
        self.hostname_changer_button.setGeometry(QRect(120, 140, 30, 30))
        self.hostname_changer_button.setStyleSheet(u"#hostname_changer_button {\n"
"	background: #231f1f;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icons/hostname_changer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hostname_changer_button.setIcon(icon6)
        self.dns_changer_button = QPushButton(self.centralwidget)
        self.dns_changer_button.setObjectName(u"dns_changer_button")
        self.dns_changer_button.setGeometry(QRect(200, 140, 30, 30))
        self.dns_changer_button.setStyleSheet(u"#dns_changer_button {\n"
"	background: #231f1f;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icons/dns_changer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dns_changer_button.setIcon(icon7)
        self.control_deck_label = QLabel(self.centralwidget)
        self.control_deck_label.setObjectName(u"control_deck_label")
        self.control_deck_label.setGeometry(QRect(10, 110, 90, 20))
        font5 = QFont()
        font5.setFamilies([u"Z003"])
        font5.setPointSize(13)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setStrikeOut(False)
        self.control_deck_label.setFont(font5)
        self.control_deck_label.setStyleSheet(u"#control_deck_label {\n"
"	color: white;\n"
"}")
        self.horizontal_line = QFrame(self.centralwidget)
        self.horizontal_line.setObjectName(u"horizontal_line")
        self.horizontal_line.setGeometry(QRect(100, 80, 220, 20))
        self.horizontal_line.setFrameShape(QFrame.Shape.HLine)
        self.horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.anti_mitm_button = QPushButton(self.centralwidget)
        self.anti_mitm_button.setObjectName(u"anti_mitm_button")
        self.anti_mitm_button.setGeometry(QRect(10, 190, 80, 26))
        self.anti_mitm_button.setStyleSheet(u"#anti_mitm_button {\n"
"	background: red;\n"
"	border-radius: 4px;\n"
"	border: 1px solid black;\n"
"}")
        self.run_fast_check_button = QPushButton(self.centralwidget)
        self.run_fast_check_button.setObjectName(u"run_fast_check_button")
        self.run_fast_check_button.setGeometry(QRect(200, 180, 30, 30))
        self.run_fast_check_button.setStyleSheet(u"#run_fast_check_button {\n"
"	background: #000064;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icons/run_fast_check.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run_fast_check_button.setIcon(icon8)
        self.browser_anonymizer_button = QPushButton(self.centralwidget)
        self.browser_anonymizer_button.setObjectName(u"browser_anonymizer_button")
        self.browser_anonymizer_button.setGeometry(QRect(120, 180, 30, 30))
        self.browser_anonymizer_button.setStyleSheet(u"#browser_anonymizer_button {\n"
"	background: #231f1f;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icons/browser.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.browser_anonymizer_button.setIcon(icon9)
        self.status_button = QPushButton(self.centralwidget)
        self.status_button.setObjectName(u"status_button")
        self.status_button.setGeometry(QRect(160, 180, 30, 30))
        self.status_button.setStyleSheet(u"#status_button {\n"
"	background: #231f1f;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icons/status.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.status_button.setIcon(icon10)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ghostsurf", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.logo_label.setText("")
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"Ghostsurf", None))
#if QT_CONFIG(tooltip)
        self.start_stop_button.setToolTip(QCoreApplication.translate("MainWindow", u"Start the ghostsurf", None))
#endif // QT_CONFIG(tooltip)
        self.start_stop_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(tooltip)
        self.change_ip_button.setToolTip(QCoreApplication.translate("MainWindow", u"Change my ip address", None))
#endif // QT_CONFIG(tooltip)
        self.change_ip_button.setText(QCoreApplication.translate("MainWindow", u"Change IP", None))
#if QT_CONFIG(tooltip)
        self.my_ip_button.setToolTip(QCoreApplication.translate("MainWindow", u"Display my ip address", None))
#endif // QT_CONFIG(tooltip)
        self.my_ip_button.setText(QCoreApplication.translate("MainWindow", u"My IP", None))
        self.status_header_label.setText(QCoreApplication.translate("MainWindow", u"Tor Status:", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Inactive", None))
#if QT_CONFIG(tooltip)
        self.info_button.setToolTip(QCoreApplication.translate("MainWindow", u"Display the help page", None))
#endif // QT_CONFIG(tooltip)
        self.info_button.setText("")
#if QT_CONFIG(tooltip)
        self.pandora_bomb_button.setToolTip(QCoreApplication.translate("MainWindow", u"Wipe memory", None))
#endif // QT_CONFIG(tooltip)
        self.pandora_bomb_button.setText("")
#if QT_CONFIG(tooltip)
        self.ultra_ghost_button.setToolTip(QCoreApplication.translate("MainWindow", u"Enable/Disable ghostsurf at boot", None))
#endif // QT_CONFIG(tooltip)
        self.ultra_ghost_button.setText(QCoreApplication.translate("MainWindow", u"disabled", None))
#if QT_CONFIG(tooltip)
        self.reset_button.setToolTip(QCoreApplication.translate("MainWindow", u"Reset", None))
#endif // QT_CONFIG(tooltip)
        self.reset_button.setText("")
#if QT_CONFIG(tooltip)
        self.mac_changer_button.setToolTip(QCoreApplication.translate("MainWindow", u"Change mac address", None))
#endif // QT_CONFIG(tooltip)
        self.mac_changer_button.setText("")
#if QT_CONFIG(tooltip)
        self.log_shredder_button.setToolTip(QCoreApplication.translate("MainWindow", u"Shred log files", None))
#endif // QT_CONFIG(tooltip)
        self.log_shredder_button.setText("")
#if QT_CONFIG(tooltip)
        self.hostname_changer_button.setToolTip(QCoreApplication.translate("MainWindow", u"Change hostname", None))
#endif // QT_CONFIG(tooltip)
        self.hostname_changer_button.setText("")
#if QT_CONFIG(tooltip)
        self.dns_changer_button.setToolTip(QCoreApplication.translate("MainWindow", u"Change nameservers", None))
#endif // QT_CONFIG(tooltip)
        self.dns_changer_button.setText("")
        self.control_deck_label.setText(QCoreApplication.translate("MainWindow", u"Control Deck", None))
        self.anti_mitm_button.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
#if QT_CONFIG(tooltip)
        self.run_fast_check_button.setToolTip(QCoreApplication.translate("MainWindow", u"Run checklist", None))
#endif // QT_CONFIG(tooltip)
        self.run_fast_check_button.setText("")
#if QT_CONFIG(tooltip)
        self.browser_anonymizer_button.setToolTip(QCoreApplication.translate("MainWindow", u"Anonymize browser", None))
#endif // QT_CONFIG(tooltip)
        self.browser_anonymizer_button.setText("")
#if QT_CONFIG(tooltip)
        self.status_button.setToolTip(QCoreApplication.translate("MainWindow", u"Update tor status", None))
#endif // QT_CONFIG(tooltip)
        self.status_button.setText("")
    # retranslateUi

