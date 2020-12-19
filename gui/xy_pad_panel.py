
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen
from PyQt5.QtCore import pyqtSlot, Qt

from gui.custom_button import CustomButton

from common import *

NEED_UPDATE_AMOUNT_X = 2
NEED_UPDATE_AMOUNT_Y = 2

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
        return self.padFrame.x * 180 / self.padFrame.width

    def getYscaled(self):
        return self.padFrame.y * 180 / self.padFrame.height


class XYPad(QtWidgets.QFrame):
    def __init__(self, parent):
        super(XYPad, self).__init__()
        self.height = 200
        self.width = 200
        self.parent = parent
        self.pressed = False
        self.lastUpdatedXScaled = 0
        self.lastUpdatedYScaled = 0
        self.x = 90
        self.y = 90
        self.xScaled = self.x * 180 / self.width
        self.yScaled = self.y * 180 / self.height
        self.setFixedSize(self.width, self.height)

    def mouseMoveEvent(self, event):
        self.updatePressedLocation(event)

    def mousePressEvent(self, event):
        print("Mouse Pressed")
        self.updatePressedLocation(event)
        self.pressed = True

    def mouseReleaseEvent(self, event):
        print("Mouse Released")
        self.pressed = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  8, Qt.SolidLine))
        painter.drawRect(0, 0, self.width, self.height)
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(self.x-2, self.y-2, 4, 4)

    def updatePressedLocation(self, event):
        x = event.x()
        y = event.y()
        if (x >= 0 and x < self.width and y >= 0 and y < self.height):
            xScaled = x * 180 / self.width
            yScaled = y * 180 / self.height
            if (abs(self.lastUpdatedXScaled - xScaled) > NEED_UPDATE_AMOUNT_X):
                self.parent.parent.clientHandle.updateX(xScaled)
                self.lastUpdatedXScaled = xScaled
            if (abs(self.lastUpdatedYScaled - yScaled) > NEED_UPDATE_AMOUNT_Y):
                self.parent.parent.clientHandle.updateY(yScaled)
                self.lastUpdatedYScaled = yScaled
            self.xScaled = xScaled
            self.yScaled = yScaled
            self.x = x
            self.y = y
            self.printLocation()
            self.repaint()

    def printLocation(self):
        print("Pad x %d, y %d (scaled x %d, y %d)" % (self.x, self.y, self.xScaled, self.yScaled))
