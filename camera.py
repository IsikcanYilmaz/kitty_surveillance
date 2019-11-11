#!/usr/bin/python3

from common import *
from picamera import PiCamera
import threading
import io
import time


class Camera:
    def __init__(self):
        self.cameraObj = PiCamera()
        self.cameraObj.resolution = (128, 128)

    # fd: file descriptor. can be a socket, or a file
    def startStream(self, fd):
        self.cameraObj.start_recording(fd, format='h264')

    def stopStream(self):
        self.cameraObj.stop_recording()


def main():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.1.100', 9998))

    print("listening for connection")
    s.listen(1)
    (conn, (ip, port)) = s.accept()
    connFile = conn.makefile('wb')
    print(conn, connFile)

    c = Camera()
    c.startStream(connFile)
    time.sleep(15)
    c.stopStream()
    print("done")

if __name__ == "__main__":
    main()
