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
from comms_packet_structure import *
sys.path.append('gui')

VLC = False


class KittyClient():
    def __init__(self):
        self.commsClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.cameraMotorThread = threading.Thread(target=self.clientCameraMotorThread)
        self.commsRxThread     = threading.Thread(target=self.clientCommsRxThread)
        #self.rxThread     = threading.Thread(target=self.clientCameraMotorThread)
        #self.txThread     = threading.Thread(target=self.clientCameraMotorThread)

        self.connected = False

        self.clientRunning = False
        self.guiRunning    = False
        self.rxRunning     = False
        self.txRunning     = False

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

    def disconnect(self):
        self.commsClientSocket.close()

    def startGui(self):
        self.guiRunning = True
        gui.client_gui.GuiThread(self)

    def clientCommsRxThread(self):
        while True:
            pass

    def clientCommsTxThread(self):
        while True:
            pass

    def clientCameraMotorThread(self):
        print("[*] clientCameraMotorThread starting")
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
                rawPacket = MakeCommsPacket(CommsPacketType.CMD_CAMERA_ANGLE_CHANGED.value, [int(self.cameraXfloat), int(self.cameraYfloat)])
                print("[*] Sending raw", [hex(i) for i in rawPacket])
                self.commsClientSocket.send(rawPacket) 

            except Exception as e:
                print("[!] clientCameraMotorThread closing", e)
                break
            time.sleep(0.1)

        self.clientRunning = False
        self.disconnect()

    # Starts the motor thread. Client must have connected priorly
    def startClient(self):
        self.clientRunning = True
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
        client.connect(commsOnly=True)
        client.startClient()
    client.startGui()

    while (client.clientRunning or client.guiRunning):
        pass

    print("[+] Done. Exiting")

if __name__ == "__main__":
    main()
