#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from gui.button_panel import *
from gui.video_panel import *


class MainWindow(QWidget):
    def __init__(self, clientHandle):
        super(MainWindow, self).__init__()
        self.clientHandle = clientHandle
        self.width = 300
        self.height = 300

        #SET WINDOW GEOMETRY
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Kitty Surveillance Client')

        #INSTANTIATE PANELS
        self.buttonPanel = ButtonPanel(self)
        self.videoPanel  = VideoPanel(self)

        #CREATE MAIN LAYOUT AND PUT IN PANELS
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.videoPanel)
        mainLayout.addWidget(self.buttonPanel)
        self.setLayout(mainLayout)

    def keyPressEvent(self, keyEvent):
        super(MainWindow, self).keyPressEvent(keyEvent)
        print(keyEvent)




def GuiThread(clientHandle):
    app = QApplication(sys.argv)
    ex = MainWindow(clientHandle)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GuiThread()
