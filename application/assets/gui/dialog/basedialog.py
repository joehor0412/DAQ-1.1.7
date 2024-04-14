#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


def set_skin(widget, qssfile):
    if os.path.exists(qssfile):
        fd = open(qssfile, "r")
        style = fd.read()
        fd.close()
        widget.setStyleSheet(style)


class BaseDialog(QtWidgets.QDialog):

    def __init__(self, styleoptions, parent=None):
        super(BaseDialog, self).__init__(parent)

        # Define main window for the application. Change options in __init__.py
        title = styleoptions['title']
        windowicon = styleoptions['windowicon']
        minsize = styleoptions['minsize']
        size = styleoptions['size']
        logo_title = styleoptions['logo_title']
        logo_img_url = styleoptions['logo_img_url']
        self.sub_title = styleoptions['sub_title']
        

        self.setWindowTitle(title)
        # self.setWindowIcon(QtGui.QIcon(windowicon))  
        # self.setMinimumSize(minsize[0], minsize[1])
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setSizeGripEnabled(False)
        self.setWindowModality( QtCore.Qt.ApplicationModal)
        self.setModal(True)
        self.setFixedSize(size[0],size[1])
        self.setStyleSheet("QDialog {background-color: rgba(177, 177, 177, 255); \
                                    border-color:  rgba(22, 22, 22, 150); \
                                    border-width: 1px; \
                                    border-radius: 8px; \
                                    color: black; \
                                    font-weight: bold;}")
        self.titlewidget = TitleTextWidget(logo_title)
        

        # Main layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(self.titlewidget)
        mainlayout.setContentsMargins(5, 5, 5, 5)
        mainlayout.setSpacing(0)
        self.setLayout(mainlayout)

        # self.resize(size[0], size[1])
        set_skin(self, 'gui/skin/qss/dialog.qss')

    """ Uncomment below to activate drag window """
    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton:
    #         self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()

    # def mouseReleaseEvent(self, event):
    #     if hasattr(self, "dragPosition"):
    #         del self.dragPosition

    # def mouseMoveEvent(self, event):
    #     if hasattr(self, "dragPosition"):
    #         if event.buttons() == QtCore.Qt.LeftButton:
    #             self.move(event.globalPos() - self.dragPosition)
    #             event.accept()


class TitleTextWidget(QtWidgets.QLabel):
    def __init__(self, text, parent=None):
        super(TitleTextWidget, self).__init__(parent)
        # label = QtWidgets.QLabel()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("QLabel {color: #B13E43; font-weight: bold; font-size: 16; qproperty-alignment: AlignCenter;}")
        self.setText(text)
        # self.setFixedSize(300, 132)
        # self.setGeometry(QtCore.QRect(100, 20, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.setFont(font)


    


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    styleoptions = {
        'title': u'退出设置',
        'windowicon': "../skin/images/ov-orange-green.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'dssssssss',
        'logo_img_url': "../skin/images/ov-orange-green.png"
    }
    dialog = BaseDialog(styleoptions)
    dialog.show()
    sys.exit(app.exec_())
