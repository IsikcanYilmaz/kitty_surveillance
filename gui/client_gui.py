#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from gui.button_panel import *
from gui.video_panel import *
from gui.xy_pad_panel import *


class MainWindow(QWidget):
    def __init__(self, clientHandle):
        super(MainWindow, self).__init__()
        self.clientHandle = clientHandle
        self.width = 600
        self.height = 500

        #SET WINDOW GEOMETRY
        #self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Kitty Surveillance Client')

        #INSTANTIATE PANELS
        self.buttonPanel = ButtonPanel(self)
        self.videoPanel  = VideoPanel(self)
        self.xyPadPanel  = XYPadPanel(self)

        #CREATE MAIN LAYOUT AND PUT IN PANELS
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.videoPanel, 0, 0, 4, 4)
        mainLayout.addWidget(self.buttonPanel,0, 4, 2, 2)
        mainLayout.addWidget(self.xyPadPanel, 2, 4, 2, 2)
        self.setLayout(mainLayout)

    def keyPressEvent(self, keyEvent):
        super(MainWindow, self).keyPressEvent(keyEvent)
        print(keyEvent)

    def updateGuiX(self):
        pass

    def updateGuiY(self):
        pass

    def startVideo(self):
        self.videoPanel.openFile("/home/jon/KODMOD/kitty_surveillance/teststream.h264")
        self.videoPanel.play()



def GuiThread(clientHandle):
    app = QApplication(sys.argv)
    ex = MainWindow(clientHandle)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GuiThread()
