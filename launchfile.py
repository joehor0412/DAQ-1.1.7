from PyQt5 import QtCore, QtGui, QtWidgets
import os
import socket
from application.version import __version__

class Ui_MainWindow(object):
    """
    A class that is in charge of the main window.
    """
    
    def setupUi(self, MainWindow):
        """
        Using the MainWindow as an input, set up the user interface, which includes creating labels and butttons.
        """
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlags( QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        MainWindow.resize(480, 330)
        #MainWindow.move(170,50)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 300, 80)) # x-coor,y-coor,x-size,y-size
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Welcome\nSelect Ventilator Model:")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 120, 380, 50))
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(50, 180, 380, 50))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.setDisabled(True)

        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(50, 240, 380, 50))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton3.setDisabled(True)

        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setGeometry(QtCore.QRect(430, 285, 130, 40)) # x-coor,y-coor,x-size,y-size
        font.setPointSize(10)
        self.versionLabel.setFont(font)
        self.versionLabel.setObjectName("vlabel")
        self.versionLabel.setText(__version__)

        self.deviceNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceNameLabel.setGeometry(QtCore.QRect(371, 310, 100, 30)) # x-coor,y-coor,x-size,y-size
        font.setPointSize(10)
        self.deviceNameLabel.setFont(font)
        self.deviceNameLabel.setObjectName("devicenamelabel")
        self.deviceNameLabel.setAlignment(QtCore.Qt.AlignRight)
        # self.deviceNameLabel.setText("XXXYYYYYZZZ")
        self.deviceNameLabel.setText(socket.gethostname())
        
        self.exitbtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitbtn.setGeometry(QtCore.QRect(430, 0, 60, 50))
        self.exitbtn.setObjectName("exitbtn")
        self.exitbtn.setStyleSheet('QPushButton{border: 0px}')
        font.setPointSize(16)
        self.exitbtn.setFont(font)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.openPuritan)
        self.pushButton2.clicked.connect(self.openSim)
        self.pushButton3.clicked.connect(self.openDemo)
        self.exitbtn.clicked.connect(self.closeapp)

    def retranslateUi(self, MainWindow):
        """
        Using the MainWindow as input, set the text for the title of the window and also for the buttons as well.
        """
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome"))
        self.pushButton.setText(_translate("MainWindow", "Puritan Bennet 980"))
        self.pushButton2.setText(_translate("MainWindow", "Retrospective Data"))
        self.pushButton3.setText(_translate("MainWindow", "Demo Mode"))
        self.exitbtn.setText(_translate("MainWindow", "X"))

    def openPuritan(self):
        #MainWindow.hide()
        os.system('python3 /home/pi/Serial/application/main.py')

    def openSim(self):
        #MainWindow.hide()
        os.system('python3 /home/pi/Serial/application/main.py -r')

    def openDemo(self):
        #MainWindow.hide()
        os.system('python3 /home/pi/Serial/application/main.py -d')

    def closeapp(self):
        QtWidgets.qApp.quit()

      


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


