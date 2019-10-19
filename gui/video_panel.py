
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class VideoPanel(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(VideoPanel, self).__init__()
        self.parent = parent

        innerLayout = QtWidgets.QGridLayout()

        self.setLayout(innerLayout)


