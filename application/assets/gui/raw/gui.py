# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("")
        MainWindow.setProperty("showMaximized()", "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QPushButton#startbtn\n"
" {\n"
"    background-color: #499F68; \n"
"    color: white; \n"
"    font-weight:bold; \n"
"    border: 1px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"} \n"
"\n"
"QPushButton:disabled#startbtn \n"
"{\n"
"    background-color:#ACD3BA;\n"
"} \n"
"\n"
"QPushButton:pressed#startbtn\n"
"{ \n"
"    background-color:#2F6643;\n"
"}\n"
"\n"
"QPushButton#stopbtn\n"
"{\n"
"    background-color: #d9534f; \n"
"    color: white;\n"
"    font-weight:bold; \n"
"    border: 1px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"} \n"
"\n"
"QPushButton:disabled#stopbtn \n"
"{\n"
"    background-color:#D5B4B6;\n"
"} \n"
"\n"
"QPushButton:pressed#stopbtn\n"
"{ \n"
"    background-color:#662429;\n"
"}\n"
"\n"
"QPushButton#exitbtn\n"
" {\n"
"    background-color: #E81123; \n"
"    color: white; \n"
"    font-weight:bold; \n"
"    border: 0px solid #E81123;\n"
"    border-radius: 5px;\n"
"} \n"
"\n"
"QPushButton:disabled#exitbtn \n"
"{\n"
"    background-color:#D5B4B6;\n"
"} \n"
"\n"
"QPushButton:pressed#exitbtn\n"
" { \n"
"    background-color:#5A2023;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 791, 491))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.main_frame.setFont(font)
        self.main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.main_frame.setObjectName("main_frame")

        self.startbtn = QtWidgets.QPushButton(self.main_frame)
        self.startbtn.setGeometry(QtCore.QRect(600, 380, 190, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.startbtn.setFont(font)
        self.startbtn.setAutoFillBackground(False)
        self.startbtn.setStyleSheet("")
        self.startbtn.setObjectName("startbtn")

        self.label = QtWidgets.QLabel(self.main_frame)
        self.label.setGeometry(QtCore.QRect(600, 283, 191, 31))
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setText("")
        self.label.setObjectName("label")
        self.graphWidget = GraphicsLayoutWidget(self.main_frame)
        self.graphWidget.setGeometry(QtCore.QRect(-11, -1, 599, 491))
        self.graphWidget.setObjectName("graphWidget")
        self.information_groupBox = QtWidgets.QGroupBox(self.main_frame)
        self.information_groupBox.setGeometry(QtCore.QRect(600, 10, 191, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.information_groupBox.setFont(font)
        self.information_groupBox.setFlat(False)
        self.information_groupBox.setCheckable(False)
        self.information_groupBox.setObjectName("information_groupBox")
        self.temp_pic_label = QtWidgets.QLabel(self.information_groupBox)
        self.temp_pic_label.setEnabled(True)
        self.temp_pic_label.setGeometry(QtCore.QRect(10, 60, 30, 30))
        self.temp_pic_label.setStyleSheet("image: url(:/UI/image.png);")
        self.temp_pic_label.setText("")
        self.temp_pic_label.setObjectName("temp_pic_label")
        self.temperature_label = QtWidgets.QLabel(self.information_groupBox)
        self.temperature_label.setGeometry(QtCore.QRect(50, 60, 131, 30))
        self.temperature_label.setObjectName("temperature_label")
        self.mem_pic_label = QtWidgets.QLabel(self.information_groupBox)
        self.mem_pic_label.setGeometry(QtCore.QRect(10, 90, 30, 30))
        self.mem_pic_label.setStyleSheet("image:url(:/UI/memory.png)")
        self.mem_pic_label.setText("")
        self.mem_pic_label.setObjectName("mem_pic_label")
        self.memory_label = QtWidgets.QLabel(self.information_groupBox)
        self.memory_label.setGeometry(QtCore.QRect(50, 95, 131, 21))
        self.memory_label.setObjectName("memory_label")
        self.cpu_pic_label = QtWidgets.QLabel(self.information_groupBox)
        self.cpu_pic_label.setGeometry(QtCore.QRect(10, 120, 30, 30))
        self.cpu_pic_label.setStyleSheet("image: url(:/UI/cpu.png);")
        self.cpu_pic_label.setText("")
        self.cpu_pic_label.setObjectName("cpu_pic_label")
        self.cpu_label = QtWidgets.QLabel(self.information_groupBox)
        self.cpu_label.setGeometry(QtCore.QRect(50, 130, 131, 21))
        self.cpu_label.setObjectName("cpu_label")
        self.time_pic_label = QtWidgets.QLabel(self.information_groupBox)
        self.time_pic_label.setGeometry(QtCore.QRect(10, 30, 25, 25))
        self.time_pic_label.setStyleSheet("image: url(:/UI/time.png);")
        self.time_pic_label.setText("")
        self.time_pic_label.setObjectName("time_pic_label")
        self.time_label = QtWidgets.QLabel(self.information_groupBox)
        self.time_label.setGeometry(QtCore.QRect(50, 35, 131, 16))
        self.time_label.setObjectName("time_label")

        self.version_label = QtWidgets.QLabel(self.centralwidget)
        self.version_label.setGeometry(QtCore.QRect(760, 465, 55, 16))
        self.version_label.setText("")
        self.version_label.setObjectName("version_label")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.version_label.setFont(font)

        self.patient_pic_label = QtWidgets.QLabel(self.main_frame)
        self.patient_pic_label.setGeometry(QtCore.QRect(600, 328, 30, 30))
        self.patient_pic_label.setStyleSheet("image:url(:/UI/patient.jpg)")
        self.patient_pic_label.setText("")
        self.patient_pic_label.setObjectName("patient_pic_label")
        self.patient_label = QtWidgets.QLabel(self.main_frame)
        self.patient_label.setGeometry(QtCore.QRect(635, 333, 81, 21))
        self.patient_label.setObjectName("patient_label")

        self.patient_button = QtWidgets.QPushButton(self.main_frame)
        self.patient_button.setGeometry(QtCore.QRect(720, 330, 61, 31))
        self.patient_button.setText("")
        self.patient_button.setObjectName("patient_button")

        self.exitbtn = QtWidgets.QPushButton(self.main_frame)
        self.exitbtn.setGeometry(QtCore.QRect(760, 0, 31, 28))
        self.exitbtn.setObjectName("exitbtn")
        self.speed_label = QtWidgets.QLabel(self.main_frame)
        self.speed_label.setGeometry(QtCore.QRect(600, 370, 51, 21))
        self.speed_label.setText("")
        self.speed_label.setObjectName("speed_label")
        self.stream_groupBox = QtWidgets.QGroupBox(self.main_frame)
        self.stream_groupBox.setGeometry(QtCore.QRect(600, 180, 191, 91))
        self.stream_groupBox.setObjectName("stream_groupBox")

        self.stream_pic_label = QtWidgets.QLabel(self.stream_groupBox)
        self.stream_pic_label.setGeometry(QtCore.QRect(10, 30, 31, 20))
        self.stream_pic_label.setObjectName("stream_pic_label")
        self.stream_pic_label.setStyleSheet("color: #393939;font:15px bold")

        self.stream_pic_label_2 = QtWidgets.QLabel(self.stream_groupBox)
        self.stream_pic_label_2.setGeometry(QtCore.QRect(10, 60, 41, 20))
        self.stream_pic_label_2.setObjectName("stream_pic_label_2")
        self.stream_pic_label_2.setStyleSheet("color: #393939;font:15px bold")

        self.stream_label_remote = QtWidgets.QLabel(self.stream_groupBox)
        self.stream_label_remote.setGeometry(QtCore.QRect(50, 30, 131, 20))
        self.stream_label_remote.setText("__._")
        self.stream_label_remote.setObjectName("stream_label")
        self.stream_label_remote.setStyleSheet("color: #060606;font:20px bold")

        self.stream_label_local = QtWidgets.QLabel(self.stream_groupBox)
        self.stream_label_local.setGeometry(QtCore.QRect(50, 60, 131, 20))
        self.stream_label_local.setText("__._")
        self.stream_label_local.setObjectName("stream_label_local")
        self.stream_label_local.setStyleSheet("color: #060606;font:20px bold")

        self.Ers_unit_label = QtWidgets.QLabel(self.stream_groupBox)
        self.Ers_unit_label.setGeometry(QtCore.QRect(115, 33, 131, 20))
        self.Ers_unit_label.setText("cmH<sub>2</sub>O/l")
        self.Ers_unit_label.setObjectName("Ers_unit_label")
        self.Ers_unit_label.setStyleSheet("color: #393939;font:13px bold")

        self.Rrs_unit_label = QtWidgets.QLabel(self.stream_groupBox)
        self.Rrs_unit_label.setGeometry(QtCore.QRect(115, 63, 131, 20))
        self.Rrs_unit_label.setText("cmH<sub>2</sub>O·s/l")
        self.Rrs_unit_label.setObjectName("Rrs_unit_label")
        self.Rrs_unit_label.setStyleSheet("color: #393939;font:13px bold")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startbtn.setText(_translate("MainWindow", "Start"))
        self.information_groupBox.setTitle(_translate("MainWindow", "CARE v1.1.5"))
        self.temperature_label.setText(_translate("MainWindow", "Temperature"))
        self.memory_label.setText(_translate("MainWindow", "Memory"))
        self.cpu_label.setText(_translate("MainWindow", "CPU Usage"))
        self.time_label.setText(_translate("MainWindow", "Time"))
        self.patient_label.setText(_translate("MainWindow", "Patient No:"))
        self.exitbtn.setText(_translate("MainWindow", "X"))
        self.stream_groupBox.setTitle(_translate("MainWindow", "Stream Status"))
        self.stream_pic_label.setText(_translate("MainWindow", "E<sub>rs</sub>:"))
        self.stream_pic_label_2.setText(_translate("MainWindow", "R<sub>rs</sub>:"))

from pyqtgraph import GraphicsLayoutWidget
import assets.gui.raw.logo_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

