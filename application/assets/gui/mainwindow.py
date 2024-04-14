#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QPushButton
from .raw.gui import Ui_MainWindow
from logclass import *
from .dialog import styleoptions, confirm, two_option_dialog, two_option_dialog_custom, timed_dialog
from version import __version__


__hostname__ = socket.gethostname()


class Ui_Main(Ui_MainWindow):

    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlags( QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

        # Initialise text
        self.version_label.setText(__version__)
        self.information_groupBox.setTitle(__hostname__)
        self.stream_groupBox.setTitle("Mechanics")

        # Define pressure plot
        self.pressure_plot = self.graphWidget.addPlot(row=0,col=1, rowspan=1, colspan=1)
        self.pressure_plot.setTitle("Pressure")
        self.pressure_plot.hideButtons()
        self.pressure_plot.setLabel('left', "cmH2O")
        self.pressure_plot.setLabel('bottom',"time(s)")
        self.pressure_plot.setXRange(0, 8, padding=0)
        self.pressure_plot.setYRange(0,60,padding=0)
        self.pressure_plot.setLimits(xMax=8,xMin=0,yMin=0,yMax=60)

        # Define flow plot
        self.flow_plot = self.graphWidget.addPlot(row=1,col=1, rowspan=1, colspan=1)
        self.flow_plot.setLabel('left',"l/min")
        self.flow_plot.setTitle("Flow")
        self.flow_plot.hideButtons()
        self.flow_plot.setLabel('bottom',"time(s)")
        self.flow_plot.setXRange(0, 8, padding=0)
        self.flow_plot.setYRange(-50, 50, padding=0)
        self.flow_plot.setLimits(xMax=8,xMin=0,yMin=-50,yMax=50)

        # Connect buttons
        self.startbtn.clicked.connect(self.control_start_stop)
        self.patient_button.clicked.connect(self.open_numpad)
        self.exitbtn.clicked.connect(self.exit_app)

        # Create logging thread
        self.log_thread = QtCore.QThread()
        self.log_worker = Log_Worker()
        self.log_worker.moveToThread(self.log_thread)
        self.log_thread.started.connect(self.log_worker.task)
        self.log_worker.finished.connect(self.log_thread.quit)

        # Create timer to update gui information.
        self.timer = QtCore.QTimer() 
        self.timer.setInterval(1000) # 1 second interval
        self.timer.timeout.connect(self.update_device_info)
        self.timer.start()

        # Create timer to save data automatically.
        self.save_timer = QtCore.QTimer() # timer to save data
        self.save_timer.setInterval(1000*600) # 10 minutes interval
        self.save_timer.timeout.connect(self.savedata)

        

    def display_retro(self):
        """ Add label to show operating in retro mode """
        self.retro_label = QtWidgets.QLabel(self.main_frame)
        self.retro_label.setGeometry(QtCore.QRect(673, 175, 107, 29))
        self.retro_label.setText("Retrospective")
        self.retro_label.setObjectName("retro_label")
        self.retro_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.retro_label.setStyleSheet("background-color: #00D8D8; border: 1px solid #00D8D8")

    def display_demo(self):
        """ Add label to show operating in demo mode """
        self.demo_label = QtWidgets.QLabel(self.main_frame)
        self.demo_label.setGeometry(QtCore.QRect(673, 175, 107, 29))
        self.demo_label.setText("DEMO MODE")
        self.demo_label.setObjectName("demo_label")
        self.demo_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.demo_label.setStyleSheet("background-color: #00D8D8; border: 1px solid #00D8D8;color: #F80000;font:bold")
