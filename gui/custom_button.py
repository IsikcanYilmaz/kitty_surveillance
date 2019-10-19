
from PyQt5 import QtWidgets

class CustomButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super(CustomButton, self).__init__(text)
