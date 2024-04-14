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


class TwoOptionDialogCustom(BaseDialog):
    def __init__(self, styleoptions, dlg_text, parent=None):
        super(TwoOptionDialogCustom, self).__init__(styleoptions, parent)
        
        # 退出设置
        self.msglabel = QtWidgets.QLabel()
        self.msglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.msglabel.setStyleSheet("QLabel {color: #3e3e41; font-weight: bold; font-size: 25;}")
        self.msglabel.setText(self.sub_title)

        # 退出设置
        self.msglabel2 = QtWidgets.QLabel()
        self.msglabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.msglabel2.setStyleSheet("QLabel {color: blue; font-weight: bold; font-size: 40;}")
        self.msglabel2.setText(dlg_text)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.msglabel2.setFont(font)

        #确认按钮布局
        self.enterwidget = QtWidgets.QWidget()
        self.pbEnter = QtWidgets.QPushButton(styleoptions['true_btn']['text'], self)
        self.pbEnter.setFixedSize(styleoptions['true_btn']['size'][0],styleoptions['true_btn']['size'][1])
        self.pbCancel = QtWidgets.QPushButton(styleoptions['false_btn']['text'], self)
        self.pbCancel.setFixedSize(styleoptions['false_btn']['size'][0],styleoptions['false_btn']['size'][1])
        self.pbEnter.clicked.connect(self.exit)
        self.pbCancel.clicked.connect(self.close)

        enterwidget_mainlayout = QtWidgets.QGridLayout()
        enterwidget_mainlayout.addWidget(self.pbEnter, 0, 0)
        enterwidget_mainlayout.addWidget(self.pbCancel, 0, 1)
        self.enterwidget.setLayout(enterwidget_mainlayout)

        self.layout().addWidget(self.msglabel2)
        self.layout().addWidget(self.msglabel)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())


    def exit(self):
        self.accept()
        


def two_option_dialog_custom(options,dlg_text,parent):
    """返回True或False"""
    dialog = TwoOptionDialogCustom(options,dlg_text,parent)
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
