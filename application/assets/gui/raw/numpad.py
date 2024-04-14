# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Wayne\Desktop\numpad.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
#
# Note: (18/2/2022) Original ui file lost. All changes to be made directly to this file
#

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 442)
        Dialog.setStyleSheet("QDialog {background-color: rgba(177, 177, 177, 255);border-radius: 5px;}\n"
"\n"
"QPushButton {font: 87 23pt \"Arial Black\";font-weight:bold; }\n"
"\n"
"QPushButton#closewindowbtn {font: 87 20pt \"Segoe UI Black\";font-weight:bold;background-color: #E81123; color: white;border: 1px solid #f44336;border-radius: 2px;}\n"
"\n"
"QPushButton#pushButton_T {font: 87 20pt \"Segoe UI Black\";font-weight:bold;background-color: #ADDCFF; border: 1px solid #8f8f91;border-radius: 6px; }\n"
"QPushButton:disabled#pushButton_T {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_T { background-color:#868686;color:#EBF6FF;}\n"
"\n"
"QPushButton#pushButton_C {font: 87 20pt \"Segoe UI Black\";font-weight:bold;background-color: #ADDCFF; border: 1px solid #8f8f91;border-radius: 6px;}\n"
"QPushButton:disabled#pushButton_C {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_C { background-color:#868686;color:#EBF6FF;}\n"
"\n"
"QPushButton#pushButton_I {font: 87 18pt \"Segoe UI Black\";font-weight:bold;background-color: #ADDCFF; border: 1px solid #8f8f91;border-radius: 6px;}\n"
"QPushButton:disabled#pushButton_I {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_I { background-color:#868686;color:#EBF6FF;}\n"
"\n"
"QPushButton#pushButton_confirm {font: 87 20pt \"Segoe UI Black\";font-weight:bold;background-color: #DCDCDC; color: green; border: 1px solid #8f8f91;border-radius: 6px;} QPushButton:disabled#pushButton_confirm {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_confirm { background-color:#868686;}\n"
"\n"
"QPushButton#pushButton_backspace {background-color: #DCDCDC; color: black; border: 1px solid #8f8f91;border-radius: 6px;} QPushButton:disabled#pushButton_backspace {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_backspace { background-color:#868686;}\n"
"\n"
"QPushButton#pushButton_clear {font: 87 20pt \"Segoe UI Black\";font-weight:bold;background-color: #DCDCDC; color: black; border: 1px solid #8f8f91;border-radius: 6px;} QPushButton:disabled#pushButton_clear {color:#90A6AC;} \n"
"QPushButton:pressed#pushButton_clear { background-color:#868686;}")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 474, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.frame.setObjectName("frame")

        self.closewindowbtn = QtWidgets.QPushButton(self.frame)
        self.closewindowbtn.setGeometry(QtCore.QRect(431, 0, 40, 31))
        self.closewindowbtn.setObjectName("closewindowbtn")

        self.titlebar = QtWidgets.QLabel(self.frame)
        self.titlebar.setGeometry(QtCore.QRect(0, 0, 471, 31))
        self.titlebar.setStyleSheet("background-color: #38618C;color:white;border-radius: 5px;\n"
                                    "font: 75 12pt \"Arial Black\";")
        self.titlebar.setObjectName("titlebar")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 40, 461, 46))
        self.label.setMaximumSize(QtCore.QSize(16777215, 46))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(21)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 87 21pt \"Arial Black\";font-weight:bold; ")
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")

        self.titlebar.raise_()
        self.closewindowbtn.raise_()
        self.label.raise_()
        self.verticalLayout.addWidget(self.frame)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_1.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 2, 1, 1)
        self.pushButton_C = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_C.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_C.setObjectName("pushButton_C")
        self.gridLayout.addWidget(self.pushButton_C, 1, 3, 1, 2)
        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 2, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 2, 1, 1)
        self.pushButton_I = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_I.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_I.setObjectName("pushButton_I")
        self.gridLayout.addWidget(self.pushButton_I, 2, 3, 1, 2)
        self.pushButton_clear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_clear.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.gridLayout.addWidget(self.pushButton_clear, 3, 0, 1, 1)
        self.pushButton_0 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_0.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_0.setObjectName("pushButton_0")
        self.gridLayout.addWidget(self.pushButton_0, 3, 1, 1, 1)
        self.pushButton_backspace = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_backspace.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_backspace.setObjectName("pushButton_backspace")
        self.gridLayout.addWidget(self.pushButton_backspace, 3, 2, 1, 1)
        self.pushButton_confirm = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_confirm.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.gridLayout.addWidget(self.pushButton_confirm, 3, 3, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_3.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_T = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_T.setEnabled(True)
        self.pushButton_T.setMinimumSize(QtCore.QSize(0, 85))
        self.pushButton_T.setObjectName("pushButton_T")
        self.gridLayout.addWidget(self.pushButton_T, 0, 3, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.closewindowbtn.setText(_translate("Dialog", "X"))
        self.titlebar.setText(_translate("Dialog", " Set Patient Number"))
        self.label.setText(_translate("Dialog", "0"))
        self.pushButton_1.setText(_translate("Dialog", "1"))
        self.pushButton_2.setText(_translate("Dialog", "2"))
        self.pushButton_4.setText(_translate("Dialog", "4"))
        self.pushButton_5.setText(_translate("Dialog", "5"))
        self.pushButton_6.setText(_translate("Dialog", "6"))
        self.pushButton_C.setText(_translate("Dialog", "Control"))
        self.pushButton_7.setText(_translate("Dialog", "7"))
        self.pushButton_8.setText(_translate("Dialog", "8"))
        self.pushButton_9.setText(_translate("Dialog", "9"))
        self.pushButton_I.setText(_translate("Dialog", "Intervention"))
        self.pushButton_clear.setText(_translate("Dialog", "Clear"))
        self.pushButton_0.setText(_translate("Dialog", "0"))
        self.pushButton_backspace.setText(_translate("Dialog", "<"))
        self.pushButton_confirm.setText(_translate("Dialog", "Confirm"))
        self.pushButton_3.setText(_translate("Dialog", "3"))
        self.pushButton_T.setText(_translate("Dialog", "Testing"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

