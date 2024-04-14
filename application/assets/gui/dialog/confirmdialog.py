#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

if __name__ == '__main__':
    from basedialog import BaseDialog
else:
    from .basedialog import BaseDialog


class ConfirmDialog(BaseDialog):
    def __init__(self, styleoptions, parent=None):
        super(ConfirmDialog, self).__init__(styleoptions, parent)
        
        # Display message
        self.msglabel = QtWidgets.QLabel()
        self.msglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.msglabel.setStyleSheet("QLabel {color: #3e3e41; font-weight: bold; font-size: 25;}")
        self.msglabel.setText(self.sub_title)

        # 
        self.enterwidget = QtWidgets.QWidget()
        self.pbEnter = QtWidgets.QPushButton(u'Confirm', self)
        # self.pbCancel = QtWidgets.QPushButton(u'Cancel', self)
        self.pbEnter.clicked.connect(self.enter)
        # self.pbCancel.clicked.connect(self.close)

        enterwidget_mainlayout = QtWidgets.QGridLayout()
        enterwidget_mainlayout.addWidget(self.pbEnter, 0, 0)
        # enterwidget_mainlayout.addWidget(self.pbCancel, 0, 1)
        self.enterwidget.setLayout(enterwidget_mainlayout)

        self.layout().addWidget(self.msglabel)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())

    def enter(self):
        self.accept()  # close dialog box, return 1


def confirm(styleoptions,parent):
    """返回True或False"""
    dialog = ConfirmDialog(styleoptions,parent)
    if dialog.exec_():
        return True
    else:
        return False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    styleoptions = {
        'title': u'Title',
        'windowicon': "../skin/images/ov-orange-green.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'Logo',
        'logo_img_url': "../skin/images/ov-orange-green.png"
    }
    print(confirm('running', styleoptions))
    sys.exit(app.exec_())
