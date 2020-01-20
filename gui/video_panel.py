
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoPanel(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(VideoPanel, self).__init__()
        self.height = 128 * 4
        self.width  = 128 * 4
        self.parent = parent

        self.setFixedSize(self.width, self.height)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        innerLayout = QtWidgets.QGridLayout()
        innerLayout.addWidget(videoWidget)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.error.connect(self.handleError)
        self.setLayout(innerLayout)

    def openFile(self, filename):
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(filename)))

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def handleError(self):
        pass
