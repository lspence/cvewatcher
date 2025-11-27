# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/icon/cve-watcher-icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionExport_to_Pdf = QAction(MainWindow)
        self.actionExport_to_Pdf.setObjectName(u"actionExport_to_Pdf")
        self.actionCVE_Id = QAction(MainWindow)
        self.actionCVE_Id.setObjectName(u"actionCVE_Id")
        self.actionCVSS_Severity = QAction(MainWindow)
        self.actionCVSS_Severity.setObjectName(u"actionCVSS_Severity")
        self.actionKeyword_Search = QAction(MainWindow)
        self.actionKeyword_Search.setObjectName(u"actionKeyword_Search")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.action1Hour = QAction(MainWindow)
        self.action1Hour.setObjectName(u"action1Hour")
        self.action4Hours = QAction(MainWindow)
        self.action4Hours.setObjectName(u"action4Hours")
        self.action8Hours = QAction(MainWindow)
        self.action8Hours.setObjectName(u"action8Hours")
        self.action24Hours = QAction(MainWindow)
        self.action24Hours.setObjectName(u"action24Hours")
        self.action24_Hours = QAction(MainWindow)
        self.action24_Hours.setObjectName(u"action24_Hours")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionReload_Last_24_Hours = QAction(MainWindow)
        self.actionReload_Last_24_Hours.setObjectName(u"actionReload_Last_24_Hours")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        __qtablewidgetitem.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        __qtablewidgetitem1.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        __qtablewidgetitem2.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        __qtablewidgetitem3.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        __qtablewidgetitem4.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font);
        __qtablewidgetitem5.setBackground(QColor(232, 224, 205));
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QSize(320, 240))
        self.tableWidget.setMaximumSize(QSize(1024, 768))
        self.tableWidget.setBaseSize(QSize(1024, 768))
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.tableWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuHelp_2 = QMenu(self.menubar)
        self.menuHelp_2.setObjectName(u"menuHelp_2")
        self.menuPoll_Interval = QMenu(self.menuHelp_2)
        self.menuPoll_Interval.setObjectName(u"menuPoll_Interval")
        self.menuHelp_3 = QMenu(self.menubar)
        self.menuHelp_3.setObjectName(u"menuHelp_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuHelp_2.menuAction())
        self.menubar.addAction(self.menuHelp_3.menuAction())
        self.menuFile.addAction(self.actionExport_to_Pdf)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionCVE_Id)
        self.menuHelp.addAction(self.actionCVSS_Severity)
        self.menuHelp.addAction(self.actionKeyword_Search)
        self.menuHelp_2.addAction(self.actionReload_Last_24_Hours)
        self.menuHelp_2.addAction(self.menuPoll_Interval.menuAction())
        self.menuPoll_Interval.addAction(self.action1Hour)
        self.menuPoll_Interval.addAction(self.action4Hours)
        self.menuPoll_Interval.addAction(self.action8Hours)
        self.menuPoll_Interval.addAction(self.action24Hours)
        self.menuHelp_3.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CVE Watcher", None))
        self.actionExport_to_Pdf.setText(QCoreApplication.translate("MainWindow", u"Export to PDF", None))
        self.actionCVE_Id.setText(QCoreApplication.translate("MainWindow", u"CVE Id", None))
        self.actionCVSS_Severity.setText(QCoreApplication.translate("MainWindow", u"CVSS Severity", None))
        self.actionKeyword_Search.setText(QCoreApplication.translate("MainWindow", u"Keyword Search", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action1Hour.setText(QCoreApplication.translate("MainWindow", u"1 Hour", None))
        self.action4Hours.setText(QCoreApplication.translate("MainWindow", u"4 Hours", None))
        self.action8Hours.setText(QCoreApplication.translate("MainWindow", u"8 Hours", None))
        self.action24Hours.setText(QCoreApplication.translate("MainWindow", u"24 Hours", None))
        self.action24_Hours.setText(QCoreApplication.translate("MainWindow", u"24 Hours", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionReload_Last_24_Hours.setText(QCoreApplication.translate("MainWindow", u"Reload Last 24 Hrs", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"#", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Score", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"CVE ID", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Description", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Severity", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Date Published", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Search", None))
        self.menuHelp_2.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuPoll_Interval.setTitle(QCoreApplication.translate("MainWindow", u"Poll Interval", None))
        self.menuHelp_3.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

