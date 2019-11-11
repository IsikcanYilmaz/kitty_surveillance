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

VLC = True

class KittyClient():
    def __init__(self):
        # Initialize video and comms IP sockets
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

        self.cameraX = 45
        self.cameraY = 45
        self.cameraXfloat = 45.0
        self.cameraYfloat = 45.0

        self.rxBuffer = []
        self.txBuffer = []
        self.rxBufferPtr = 0
        self.txBufferPtr = 0

    def connect(self):
        #self.commsClientSocket.connect((SERVER_IP_ADDR, COMMS_IP_PORT))
        # TODO # DO SECURITY HANDSHAKE
        self.videoClientSocket.connect((SERVER_IP_ADDR, VIDEO_IP_PORT))
        self.connected = True
        print("[+] Client connected to %s successfully" % SERVER_IP_ADDR)



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
            f = open("teststream", "wb")

        while self.videoRxRunning:
            while (not self.connected):
                pass
            buf = []
            while True:
                data = self.videoClientSocket.recv(1024)
                if not data:
                    break
                else:
                    print(data)
                    if (VLC):
                        player.stdin.write(data)
                    else:
                        f.write(data)
            if (not VLC):
                f.close()

            self.videoRxRunning = False


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
                self.commsClientSocket.send(struct.pack('II', int(self.cameraXfloat), int(self.cameraYfloat)))
            except Exception as e:
                print("closing", e)
                break;
            time.sleep(0.1)

        self.clientRunning = False
        self.disconnect()

    def moveX(self, rate):
        self.cameraXfloat += rate
        print(self.cameraXfloat)

    def moveY(self, rate):
        self.cameraYfloat += rate
        print(self.cameraYfloat)

    def startClient(self):
        self.clientRunning = True
        self.videoThread.start()
        #self.clientThread.start()
        #self.rxThread.start()
        #self.txThread.start()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--gui_only', dest='gui_only', action='store_true', default=False, help='DEBUG only show gui for test purposes')

    args = parser.parse_args()
    print(args.gui_only)

    client = KittyClient()

    if (not args.gui_only):
        client.connect()
        client.startClient()
    client.startGui()

    while (client.clientRunning or client.guiRunning):
        pass

    print("Done. Exiting")

if __name__ == "__main__":
    main()
