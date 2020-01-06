#!/usr/bin/python3

from common import *
import picamera
import threading
import io
import time

from debug import *


class Camera:
    def __init__(self, resolutionX=128, resolutionY=128):
        self.resolutionX = resolutionX
        self.resolutionY = resolutionY
        self.cameraObj = picamera.PiCamera()
        self.cameraObj.resolution = (self.resolutionX, self.resolutionY)
        self.PRINT("Created camera robject with %d x %d resolution" % (resolutionX, resolutionY))

    # Wrapper for the debug print call, with the server module as argument
    def PRINT(self, string, level=0):
        debugPrint(string, DEBUG_MODULE_CAMERA, level)

    # fd: file descriptor. can be a socket, or a file
    def startStream(self, fd):
        self.cameraObj.start_recording(fd, format='h264')

    def stopStream(self):
        self.cameraObj.stop_recording()

    def getCircularBuffer(self):
        return picamera.PiCameraCircularIO(self.cameraObj, seconds = 20)

def main():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.1.149', 9998))

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
