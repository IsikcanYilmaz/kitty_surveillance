
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from gui.custom_button import CustomButton

from common import *

NEED_UPDATE_AMOUNT = 5

class XYPadPanel(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(XYPadPanel, self).__init__()
        self.parent = parent
        innerLayout = QtWidgets.QGridLayout()

        self.padFrame = XYPad(self)

        innerLayout.addWidget(self.padFrame)

        self.setLayout(innerLayout)

    def getX(self):
        return self.padFrame.x

    def getY(self):
        return self.padFrame.y

    def getXscaled(self):
        return self.padFrame.x * 180 / self.padFrame.width()

    def getYscaled(self):
        return self.padFrame.y * 180 / self.padFrame.height()


class XYPad(QtWidgets.QFrame):
    def __init__(self, parent):
        super(XYPad, self).__init__()
        self.parent = parent
        self.pressed = False
        self.lastUpdatedXScaled = 0
        self.lastUpdatedYScaled = 0
        self.xScaled = 0
        self.yScaled = 0
        self.x = 0
        self.y = 0

    def mouseMoveEvent(self, event):
        self.updatePressedLocation(event)

    def mousePressEvent(self, event):
        print("Mouse Pressed")
        self.updatePressedLocation(event)
        self.pressed = True

    def mouseReleaseEvent(self, event):
        print("Mouse Released")
        self.pressed = False

    def updatePressedLocation(self, event):
        x = event.x()
        y = event.y()
        if (x >= 0 and x < self.width() and y >= 0 and y < self.height()):
            xScaled = x * 180 / self.width()
            yScaled = y * 180 / self.height()
            if (abs(self.lastUpdatedXScaled - xScaled) > NEED_UPDATE_AMOUNT):
                self.parent.parent.clientHandle.updateX(xScaled)
                self.lastUpdatedXScaled = xScaled
            if (abs(self.lastUpdatedYScaled - yScaled) > NEED_UPDATE_AMOUNT):
                self.parent.parent.clientHandle.updateY(yScaled)
                self.lastUpdatedYScaled = yScaled
            self.xScaled = xScaled
            self.yScaled = yScaled
            self.x = x
            self.y = y
            self.printLocation()

    def printLocation(self):
        print("Pad x %d, y %d (scaled x %d, y %d)" % (self.x, self.y, self.xScaled, self.yScaled))
