#!/usr/bin/python3

import sys
import socket
import struct
import time
import gui.client_gui
import threading
import argparse
import subprocess

from common import *
sys.path.append('gui')

TCP_IP = '192.168.1.100'
TCP_PORT = 9999

VLC = False


class KittyClient():
    def __init__(self):
        # Initialize video and comms IP sockets
        if (VIDEO_OVER_UDP):
            print("[+] Video over UDP")
            self.videoClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("[+] Video over TCP")
            self.videoClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commsClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientThread = threading.Thread(target=self.clientMainThread)
        self.videoThread  = threading.Thread(target=self.videoRxThread)
        #self.rxThread     = threading.Thread(target=self.clientMainThread)
        #self.txThread     = threading.Thread(target=self.clientMainThread)

        self.connected = False

        self.clientRunning = False
        self.guiRunning    = False
        self.rxRunning     = False
        self.txRunning     = False
        self.videoRxRunning = False

        self.cameraX = 0
        self.cameraY = 0
        self.cameraXfloat = 0
        self.cameraYfloat = 0

        self.rxBuffer = []
        self.txBuffer = []
        self.rxBufferPtr = 0
        self.txBufferPtr = 0

    def connect(self):
        # FIRST CONNECT TO THE COMMS PORT
        self.commsClientSocket.connect((SERVER_IP_ADDR, COMMS_IP_PORT))
        # TODO # DO SECURITY HANDSHAKE
        time.sleep(2)

        # SET UP TCP/UDP CONNECTION
        if (VIDEO_OVER_UDP):
            print("[+] Client waiting for UDP video stream")
        else:
            self.videoClientSocket.connect((SERVER_IP_ADDR, VIDEO_IP_PORT))
            print("[+] Client connected to %s successfully" % SERVER_IP_ADDR)
        self.connected = True

    def disconnect(self):
        self.commsClientSocket.close()
        self.videoClientSocket.close()

    def startGui(self):
        self.guiRunning = True
        gui.client_gui.GuiThread(self)

    def videoRxThread(self):
        self.videoRxRunning = True
        if (VLC):
            cmdline = ['vlc', '--demux', 'h264', '-']
            player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        else:
            f = open("teststream.h264", "wb")

        while self.videoRxRunning:
            while (not self.connected):
                pass
            print("[+] Video Connected! Stream to file:", (not VLC))
            buf = []
            while True:
                if (VIDEO_OVER_UDP):
                    data, addr = self.videoClientSocket.recvfrom(1024)
                    print(data, addr)
                else:
                    data = self.videoClientSocket.recv(1024)

                if not data:
                    print("[!] Not data line 81")
                    break
                else:
                    #print(data)
                    if (VLC):
                        player.stdin.write(data)
                    else:
                        f.write(data)
            if (not VLC):
                f.close()

            self.videoRxRunning = False
            print("[+] Ending video stream")



    #def clientRxThread(self):
    #    pass

    #def clientTxThread(self):
    #    pass

    def clientMainThread(self):
        while True:
            lastCameraX = self.cameraXfloat
            lastCameraY = self.cameraYfloat

            # DONT TRANSMIT UNTIL X/Y MOVE HAPPENS
            while (lastCameraX == self.cameraXfloat and lastCameraY == self.cameraYfloat):
                pass

            # TRANSMIT NEW X AND Y
            try:
                if (self.cameraXfloat < 0):
                    self.cameraXfloat = 0
                if (self.cameraXfloat > 255):
                    self.cameraXfloat = 255

                if (self.cameraYfloat < 0):
                    self.cameraYfloat = 0
                if (self.cameraYfloat > 255):
                    self.cameraYfloat = 255
                self.commsClientSocket.send(struct.pack('II', int(self.cameraXfloat), int(self.cameraYfloat)))
            except Exception as e:
                print("closing", e)
                break;
            time.sleep(0.1)

        self.clientRunning = False
        self.disconnect()

    # TODO # PLEASE FOR THE LOVE OF GOD CLEAN THIS STUFF UP
    def setX(self, angle):
        self.cameraXfloat = angle

    def setY(self, angle):
        self.cameraYfloat = angle

    def moveX(self, rate):
        self.cameraXfloat += rate
        if self.cameraXfloat > 180:
            self.cameraXfloat = 180
        if self.cameraXfloat < 0:
            self.cameraXfloat = 0
        print(self.cameraXfloat)

    def moveY(self, rate):
        self.cameraYfloat += rate
        if self.cameraYfloat > 180:
            self.cameraYfloat = 180
        if self.cameraYfloat < 0:
            self.cameraYfloat = 0
        print(self.cameraYfloat)

    def updateX(self, x):
        self.cameraXfloat = x
        if self.cameraXfloat > 180:
            self.cameraXfloat = 180
        if self.cameraXfloat < 0:
            self.cameraXfloat = 0
        print("SETTING CLIENT X TO", self.cameraXfloat)

    def updateY(self, y):
        self.cameraYfloat = y
        if self.cameraYfloat > 180:
            self.cameraYfloat = 180
        if self.cameraYfloat < 0:
            self.cameraYfloat = 0
        print("SETTING CLIENT Y TO", self.cameraYfloat)


    def startClient(self):
        self.clientRunning = True
        self.videoThread.start()
        self.clientThread.start()
        #self.rxThread.start()
        #self.txThread.start()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--gui_only', dest='gui_only', action='store_true', default=False, help='DEBUG only show gui for test purposes')
    parser.add_argument('--camera_only', dest='camera_only', action='store_true', default=False, help='DEBUG only run the camera server')

    args = parser.parse_args()
    if (args.gui_only):
        print("GUI ONLY")

    client = KittyClient()

    if (not args.gui_only):
        client.connect()
        client.startClient()
    client.startGui()

    while (client.clientRunning or client.guiRunning):
        pass

    print("[+] Done. Exiting")

if __name__ == "__main__":
    main()
