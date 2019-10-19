#!/usr/bin/python3

import sys
import socket
import struct
import time
import gui.client_gui
import threading

sys.path.append('gui')

#TCP_IP = '192.168.1.109'
TCP_IP = '127.0.0.1'
TCP_PORT = 8888

class KittyClient():
    def __init__(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientRunning = False
        self.guiRunning    = False
        self.cameraX = 45
        self.cameraY = 45
        self.cameraXfloat = 45.0
        self.cameraYfloat = 45.0

    def connect(self, ip, port):
        self.tcpClient.connect((ip, port))

    def disconnect(self):
        self.tcpClient.close()

    def startGui(self):
        self.guiRunning = True
        gui.client_gui.GuiThread(self)

    def ClientThread(self):
        while True:
            lastCameraX = self.cameraXfloat
            lastCameraY = self.cameraYfloat

            # DONT TRANSMIT UNTIL X/Y MOVE HAPPENS
            while (lastCameraX == self.cameraXfloat and lastCameraY == self.cameraYfloat):
                pass

            try:
                self.tcpClient.send(struct.pack('II', int(self.cameraXfloat), int(self.cameraYfloat)))
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

    def startClientThread(self):
        self.clientRunning = True
        self.clientThread = threading.Thread(target=self.ClientThread)
        self.clientThread.start()


def main():
    client = KittyClient()
    client.connect(TCP_IP, TCP_PORT)
    client.startClientThread()
    client.startGui()
    while (client.clientRunning or client.guiRunning):
        pass
    print("Done. Exiting")

if __name__ == "__main__":
    main()
