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
from debug import *
from comms_packet_structure import CommsPacketType
sys.path.append('gui')

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

        self.cameraMotorThread = threading.Thread(target=self.clientCameraMotorThread)
        self.videoThread       = threading.Thread(target=self.clientVideoRxThread)
        self.commsRxThread     = threading.Thread(target=self.clientCommsRxThread)
        #self.rxThread     = threading.Thread(target=self.clientCameraMotorThread)
        #self.txThread     = threading.Thread(target=self.clientCameraMotorThread)

        self.connected = False

        self.clientRunning = False
        self.guiRunning    = False
        self.rxRunning     = False
        self.txRunning     = False
        self.videoRxRunning = False

        self.cameraXfloat = 0
        self.cameraYfloat = 0

        self.rxBuffer = []
        self.txBuffer = []
        self.rxBufferPtr = 0
        self.txBufferPtr = 0

    # Wrapper for the debug print call, with the server module as argument
    def PRINT(self, string, level=0):
        debugPrint(string, DEBUG_MODULE_CLIENT, level)


    def connect(self, commsOnly=False):
        # FIRST CONNECT TO THE COMMS PORT
        ret = self.connectComms()

        # TODO # DO SECURITY HANDSHAKE

        if (not commsOnly and ret):
            ret = self.connectVideo()
        return ret

    def connectComms(self):
        self.PRINT("Waiting for comms connection...")
        try:
            self.commsClientSocket.connect((SERVER_IP_ADDR, COMMS_IP_PORT))
            self.connected = True
            time.sleep(2)
            return True
        except Exception as e:
            self.PRINT("Couldnt connect to comms server")
            self.PRINT(e)
            return False

    def connectVideo(self):
        # SET UP TCP/UDP CONNECTION
        if (VIDEO_OVER_UDP):
            self.PRINT("Client waiting for UDP video stream")
        else:
            try:
                self.videoClientSocket.connect((SERVER_IP_ADDR, VIDEO_IP_PORT))
                self.PRINT("Client connected to %s:%d successfully" % (SERVER_IP_ADDR, VIDEO_IP_PORT))
                return True
            except Exception as e:
                self.PRINT("Couldnt connect to video server (TCP)")
                self.PRINT(e)
                return False


    def disconnect(self):
        self.commsClientSocket.close()
        self.videoClientSocket.close()

    def startGui(self):
        self.guiRunning = True
        gui.client_gui.GuiThread(self)

    def clientVideoRxThread(self):
        self.videoRxRunning = True
        if (VLC):
            cmdline = ['vlc', '--demux', 'h264', '-']
            player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        else:
            f = open("teststream.h264", "wb")

        while self.videoRxRunning:
            while (not self.connected):
                pass
            self.PRINT("Video Connected! Stream to file: %s" % (not VLC))
            buf = []
            while True:
                if (VIDEO_OVER_UDP):
                    data, addr = self.videoClientSocket.recvfrom(1024)
                    print(data, addr)
                else:
                    data = self.videoClientSocket.recv(1024)

                if not data:
                    self.PRINT("[!] Not data line 81")
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
            self.PRINT("Ending video stream")

    def clientCommsRxThread(self):
        while True:
            pass

    def clientCommsTxThread(self):
        while True:
            pass

    def clientCameraMotorThread(self):
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
                self.commsClientSocket.send(struct.pack('BBB', int(CommsPacketType.CMD_CAMERA_ANGLE_CHANGED.value), int(self.cameraXfloat), int(self.cameraYfloat)))
            except Exception as e:
                print("[!] clientCameraMotorThread closing", e)
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


    # Starts the video thread and the motor thread. Client must have connected priorly
    def startClient(self):
        self.clientRunning = True
        self.videoThread.start()
        self.cameraMotorThread.start()
        #self.rxThread.start()
        #self.txThread.start()


def main():
    print("K i t t y S u r v e i l l a n c e - Client - v%s" % (VERSION))
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
