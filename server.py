#!/usr/bin/python3

import socket
import struct
import threading
import picamera
import camera
import time

#TODO : need to redo following code
from pwm import Motors
from common import *

BUFFER_SIZE = 20


class KittyServer():
    def __init__(self, ip, video_port, comms_port):
        self.ip = ip
        self.video_port = video_port
        self.comms_port = comms_port

        self.commsServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commsServer.bind((ip, comms_port))

        if (VIDEO_OVER_UDP):
            self.videoServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.videoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.videoServer.bind((ip, video_port))

        # ServerRxThread and TxThread for the communication of commands, coordinates, etc.
        self.serverRxThread = threading.Thread(target=self.ServerRxThread)
        self.serverTxThread = threading.Thread(target=self.ServerTxThread)

        self.connectionEstablished = False
        self.clientConnection = {}

        self.cameraX = 45
        self.cameraY = 45
        self.camera = camera.Camera()

        self.cameraMotors = Motors()

    def ServerRxThread(self):
        print("[+] Server Rx thread started")
        while (self.connectionEstablished):
            rxData = self.clientConnection['commsConn'].recv(2 * 4)
            print("[+] Data received", rxData)
            self.processInput(rxData)


    def ServerTxThread(self):
        pass

    def connectionSequence(self):
        print("[SER] Waiting for connection on port %d" % (self.comms_port))
        self.commsServer.listen(1)
        (conn, (ip, port)) = self.commsServer.accept()
        self.clientConnection = {
                                "ip"       : ip,
                                "commsConn": conn,
                                "videoConn": None,
                                "running"  : False
                                }
        print("[SER] Comms port connection established with %s" % ip)
        # TODO # add security measures before opening up video server

        print("[SER] Waiting for connection on port %d" % (self.video_port))

        if (VIDEO_OVER_UDP): # IF UDP
            stream = self.camera.getCircularBuffer()
            self.camera.startStream(stream)
            while True:
                self.camera.cameraObj.wait_recording(1)
                print("stream done")
                print(stream.readall())
        else:                # IF TCP
            self.videoServer.listen(1)
            (conn, (ip, port)) = self.videoServer.accept()
            print("[SER] Video port connection established with %s" % ip)
            self.connectionEstablished = True
            self.clientConnection['running'] = True

            # BOTH COMMS AND VIDEO CONNECTIONS ESTABLISHED AT THIS POINT
            # GET FILE DESCRIPTOR OUT OF OUR CONNECTION SOCKET. WRITE VIDEO STREAM TO IT
            self.videoClient = conn
            self.videoClientFile = self.videoClient.makefile('wb')

            print("[SER] Starting stream", self.videoClient, self.videoClientFile)
            self.camera.startStream(self.videoClientFile)


    def terminateConnection(self):
        if (self.clientConnection['commsConn'] != None):
            self.clientConnection['commsConn'].close()
            self.clientConnection['commsConn'] = None
        if (self.clientConnection['videoConn'] != None):
            self.clientConnection['videoConn'].close()
            self.clientConnection['videioConn'] = None
        self.clientConnection['running'] = False
        print('[SER] Connection with %s terminated' % self.clientConnection['ip'])


    def processInput(self, data):
        unpackedData = struct.unpack('III', data)
        inputType = unpackedData[0]
        unpackedData = unpackedData[1:]

        if (unpackedData == CMD_CAMERA_ANGLE_CHANGED):
            newX = unpackedData[0]
            newY = unpackedData[1]

            if (newX < 0):
                newX = 0
            elif (newX > 180):
                newX = 180

            if (newY < 0):
                newY = 0
            elif (newY > 180):
                newY = 180

            self.cameraMotors.setX(newX)
            self.cameraMotors.setY(newY)
            print("[SER] NEW X: %d, NEW Y: %d" % (newX, newY))

    def run(self):
        self.running = True

        print("[SER] Starting kitty server")

        # MAIN LOOP
        self.connectionSequence()
        self.serverRxThread.start()
        while self.clientConnection['running']:
            pass
            #self.terminateConnection()

        print("[SER] Shutting down server")



def main():
    server = KittyServer(SERVER_IP_ADDR, VIDEO_IP_PORT, COMMS_IP_PORT)
    server.run()

if __name__ == '__main__':
    main()
