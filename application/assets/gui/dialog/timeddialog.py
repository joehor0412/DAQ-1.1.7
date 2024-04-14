#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    from basedialog import BaseDialog
else:
    from .basedialog import BaseDialog


class TwoOptionDialog(BaseDialog):
    def __init__(self, styleoptions, parent=None):
        super(TwoOptionDialog, self).__init__(styleoptions, parent)
        self.timer = QtCore.QTimer()
        self.timeout = 10
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(1000)
        self.timer.start()

        # 退出设置
        self.msglabel = QtWidgets.QLabel()
        self.msglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.msglabel.setStyleSheet("QLabel {color: #3e3e41; font-weight: bold; font-size: 25;}")
        # self.msglabel.setText(self.sub_title)
        self.msglabel.setText("No Serial Connection\nCheck serial port connection\n\nRetrying in 10 seconds")

        #确认按钮布局
        self.enterwidget = QtWidgets.QWidget()
        self.pbEnter = QtWidgets.QPushButton(u'Retry Now', self)
        self.pbEnter.setFixedSize(100,40)
        self.pbCancel = QtWidgets.QPushButton(u'Cancel', self)
        self.pbCancel.setFixedSize(100,40)
        self.pbEnter.clicked.connect(self.exit)
        self.pbCancel.clicked.connect(self.close)

        enterwidget_mainlayout = QtWidgets.QGridLayout()
        enterwidget_mainlayout.addWidget(self.pbEnter, 0, 0)
        enterwidget_mainlayout.addWidget(self.pbCancel, 0, 1)
        self.enterwidget.setLayout(enterwidget_mainlayout)

        self.layout().addWidget(self.msglabel)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())

    def tick(self):
        self.timeout -= 1
        if self.timeout >= 0:
            self.msglabel.setText("No Serial Connection\nCheck serial port connection\n\nRetrying in %i seconds" % self.timeout)
        else:
            self.timer.stop()
            self.exit()


    def exit(self):
        self.accept()
        


def timed_dialog(options,parent):
    """返回True或False"""
    dialog = TwoOptionDialog(options,parent)
    if dialog.exec_():
        return True
    else:
        return False

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    styleoptions = {
        'title': u'退出设置',
        'windowicon': "../skin/images/ov-orange-green.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': "../skin/images/ov-orange-green.png"
    }
    print(exit(styleoptions))
    sys.exit(app.exec_())
