from PyQt5 import QtCore, QtGui, QtWidgets
from assets.gui.raw.numpad import Ui_Dialog


class Numpad_New(Ui_Dialog):

    def __init__(self, parent=None):
        super(Numpad_New, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags( QtCore.Qt.FramelessWindowHint)
        self.setSizeGripEnabled(False)
        self.setWindowModality( QtCore.Qt.ApplicationModal)
        self.setModal(True)
        self.setFixedSize(472, 442)
        self.move(150,20)
        self.set_keypad_disabled_state(True)
        self.set_control_disabled_state(True)
        
        for n in range(0, 10):
            getattr(self, 'pushButton_%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        self.closewindowbtn.clicked.connect(self.close)
        self.pushButton_C.clicked.connect(self.set_file_header)
        self.pushButton_T.clicked.connect(self.set_file_header)
        self.pushButton_I.clicked.connect(self.set_file_header)
        self.pushButton_confirm.clicked.connect(self.confirm_input)
        self.pushButton_clear.clicked.connect(self.clear_input)
        self.pushButton_backspace.clicked.connect(self.backspace_input)

    def set_file_header(self):
        button = self.sender()
        text = button.text()
        if text == "Control":
            self.label.setText('C0000')
        elif text == "Testing":
            self.label.setText('T0000')
        else:
            self.label.setText('I0000')
        self.set_option_disabled_state(True)
        self.set_keypad_disabled_state(False)
        self.pushButton_clear.setDisabled(False)
        self.pushButton_backspace.setDisabled(False)

    def input_number(self,number):
        input_number = str(number)
        label_num = int(str(self.label.text()).lstrip("CTI")) # get the value of previous label input
        if label_num < 1000:
            label = list(str(self.label.text()))
            label[-4] = label[-3]
            label[-3] = label[-2]
            label[-2] = label[-1]
            label[-1] = input_number
            self.label.setText("".join(label))
        self.pushButton_confirm.setDisabled(False)
        self.pushButton_backspace.setDisabled(False)

    def backspace_input(self):
        label_num = int(str(self.label.text()).lstrip("CTI"))
        label = list(str(self.label.text()))
        label[-1] = label[-2]
        label[-2] = label[-3]
        label[-3] = label[-4]
        label[-4] = "0"
        self.label.setText("".join(label))
        if int(str(self.label.text()).lstrip("CTI")) == 0:
            self.pushButton_confirm.setDisabled(True)

    def confirm_input(self):
        self.text = self.label.text()
        self.accept()
        
    def clear_input(self):
        self.set_control_disabled_state(True)
        self.set_keypad_disabled_state(True)
        self.set_option_disabled_state(False)
        self.label.setText("")

    def set_control_disabled_state (self,state):
        self.pushButton_confirm.setDisabled(state)
        self.pushButton_clear.setDisabled(state)
        self.pushButton_backspace.setDisabled(state)

    def set_option_disabled_state (self,state):
        self.pushButton_C.setDisabled(state)
        self.pushButton_T.setDisabled(state)
        self.pushButton_I.setDisabled(state)

    def set_keypad_disabled_state (self,state):
        self.pushButton_1.setDisabled(state)
        self.pushButton_2.setDisabled(state)
        self.pushButton_3.setDisabled(state)
        self.pushButton_4.setDisabled(state)
        self.pushButton_5.setDisabled(state)
        self.pushButton_6.setDisabled(state)
        self.pushButton_7.setDisabled(state)
        self.pushButton_8.setDisabled(state)
        self.pushButton_9.setDisabled(state)
        self.pushButton_0.setDisabled(state)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = Numpad_New()
    Dialog.show()
    sys.exit(app.exec_())
    