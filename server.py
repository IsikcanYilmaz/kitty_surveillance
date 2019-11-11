#!/usr/bin/python3

import socket
import struct
import threading
import camera
import time

#TODO : need to redo following code
from pwm import Motors
from common import *

BUFFER_SIZE = 20

class KittyServer():
    def __init__(self, ip, video_port, comms_port):
        self.commsServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commsServer.bind((ip, comms_port))
        self.videoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.videoServer.bind((ip, video_port))

        self.serverRxThread = threading.Thread(target=self.ServerTxThread)
        self.serverTxThread = threading.Thread(target=self.ServerRxThread)

        self.clientConnection = {}

        self.cameraX = 45
        self.cameraY = 45
        self.camera = camera.Camera()

        #self.motors = Motors()

    def ServerRxThread(self):

        pass

    def ServerTxThread(self):
        pass

    def connectionSequence(self):
        print("[+] Waiting for connection")
        self.commsServer.listen(1)
        (conn, (ip, port)) = self.commsServer.accept()
        self.clientConnection = {
                                "ip"       : ip,
                                "commsConn": conn,
                                "videoConn": None,
                                "running"  : False
                                }
        print("[+] Comms port connection established with %s" % ip)
        # TODO # add security measures before opening up video server
        self.videoServer.listen(1)
        (conn, (ip, port)) = self.videoServer.accept()
        print("[+] Video port connection established with %s" % ip)


    def terminateConnection(self):
        if (self.clientConnection['commsConn'] != None):
            self.clientConnection['commsConn'].close()
            self.clientConnection['commsConn'] = None
        if (self.clientConnection['videoConn'] != None):
            self.clientConnection['videoConn'].close()
            self.clientConnection['videioConn'] = None
        self.clientConnection['running'] = False
        print('[+] Connection with %s terminated' % self.clientConnection['ip'])


    def receiveInput(self, data):
        unpackedData = struct.unpack('II', data)
        newX = unpackedData[0]
        newY = unpackedData[1]
        self.motors.setX(newX)
        self.motors.setY(newY)
        print("NEW X: %d, NEW Y: %d" % (newX, newY))

    def run(self):
        self.running = True

        print("[+] Starting kitty server")

        # MAIN LOOP
        self.connectionSequence()
        while self.clientConnection['running']:
            self.terminateConnection()



def main():
    server = KittyServer(SERVER_IP_ADDR, VIDEO_IP_PORT, COMMS_IP_PORT)
    server.run()

if __name__ == '__main__':
    main()
