
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from gui.custom_button import CustomButton

from common import *

LEFT_PRESS  = 0
RIGHT_PRESS = 1
UP_PRESS    = 2
DOWN_PRESS  = 3


class ButtonPanel(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(ButtonPanel, self).__init__()
        self.parent = parent
        innerLayout = QtWidgets.QGridLayout()

        self.leftButton  = CustomButton("<-")
        self.rightButton = CustomButton("->")
        self.upButton    = CustomButton("^")
        self.downButton  = CustomButton("v")

        self.leftButton.clicked.connect(lambda: self.buttonPushed(LEFT_PRESS))
        self.rightButton.clicked.connect(lambda: self.buttonPushed(RIGHT_PRESS))
        self.upButton.clicked.connect(lambda: self.buttonPushed(UP_PRESS))
        self.downButton.clicked.connect(lambda: self.buttonPushed(DOWN_PRESS))

        innerLayout.addWidget(self.upButton,     0, 0)
        innerLayout.addWidget(self.downButton,   0, 1)
        innerLayout.addWidget(self.leftButton,   1, 0)
        innerLayout.addWidget(self.rightButton,  1, 1)

        self.setLayout(innerLayout)


    def buttonPushed(self, button):
        print("%d PRESSED" % button)
        if button == LEFT_PRESS:
            self.parent.clientHandle.moveX(-GUI_INCREMENT_RATE)
        if button == RIGHT_PRESS:
            self.parent.clientHandle.moveX(GUI_INCREMENT_RATE)
        if button == UP_PRESS:
            self.parent.clientHandle.moveY(GUI_INCREMENT_RATE)
        if button == DOWN_PRESS:
            self.parent.clientHandle.moveY(-GUI_INCREMENT_RATE)



