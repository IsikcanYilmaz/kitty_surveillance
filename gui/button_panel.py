
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

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

        self.videoTestButton = CustomButton("Video Test")
        self.videoTestButton.clicked.connect(lambda: self.parent.startVideo())

        self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.slider.setMinimum = 0
        self.slider.setMaximum = 180

        innerLayout.addWidget(self.upButton,     0, 0)
        innerLayout.addWidget(self.downButton,   0, 1)
        innerLayout.addWidget(self.leftButton,   1, 0)
        innerLayout.addWidget(self.rightButton,  1, 1)
        innerLayout.addWidget(self.slider,       2, 0, 2, 2)
        innerLayout.addWidget(self.videoTestButton, 3, 0)

        self.slider.valueChanged.connect(self.sliderValueChanged)

        self.setLayout(innerLayout)

    def sliderValueChanged(self):
        print("[*] Slider changed:", self.slider.value())
        self.parent.clientHandle.setX(self.slider.value())

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



