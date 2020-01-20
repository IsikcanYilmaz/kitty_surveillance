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
from debug import *
from comms_packet_structure import CommsPacketType

BUFFER_SIZE = 20

class KittyServer():
    def __init__(self, ip, video_port, comms_port):
        self.ip = ip
        self.video_port = video_port
        self.comms_port = comms_port
        self.running = False
        #self.initialize()

    # Wrapper for the debug print call, with the server module as argument
    def PRINT(self, string, level=0):
        debugPrint(string, DEBUG_MODULE_SERVER, level)

    # This actually does the initialization.
    # initializes threads. the starting of them is done in run()
    # After a disconnected client, one should terminateConnections,
    # deinitialize, and initialize again.
    def initialize(self):
        self.commsServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commsServer.bind((self.ip, self.comms_port))

        if (VIDEO_OVER_UDP):
            self.videoServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.videoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.videoServer.bind((self.ip, self.video_port))

        # ServerRxThread and TxThread for the communication of commands, coordinates, etc.
        self.serverRxThread = threading.Thread(target=self.ServerRxThread)
        self.serverTxThread = threading.Thread(target=self.ServerTxThread)

        self.connectionEstablished = False
        self.clientConnection = {}

        self.cameraX = 45
        self.cameraY = 45
        self.camera = camera.Camera(512, 512)

        self.cameraMotors = Motors()

    # Joins threads, destroys camera and motor objects. Add anything else if you think of any
    def deinitialize(self):
        self.serverRxThread.join()
        self.serverTxThread.join()
        del(self.camera)
        del(self.cameraMotors)

    # This thread continuously receives data, passes to processInput
    # TODO: Currently there's one size in receiving. have this
    def ServerRxThread(self):
        self.PRINT("Server Rx thread started")
        while (self.connectionEstablished):
            rxData = self.clientConnection['commsConn'].recv(2 * 4)
            if (rxData):
                self.processInput(rxData)
            else:
                pass
                #self.PRINT("[!] No Data received.")
                #self.terminateConnections() # This will have the thread complete


    def ServerTxThread(self):
        pass

    # Connect to client thru COMMS and then VIDEO connections.
    # TODO: have this sequence be an exchange between the client and server.
    # TODO: have some ssl key check trickery
    def connectionSequence(self):
        self.PRINT("Waiting for connection on port %s:%d" % (self.ip, self.comms_port))
        self.commsServer.listen(1)
        (conn, (ip, port)) = self.commsServer.accept()
        self.clientConnection = {
                                "ip"       : ip,
                                "commsConn": conn,
                                "videoConn": None,
                                "running"  : False
                                }
        self.PRINT("Comms port connection established with %s" % ip)
        # TODO # add security measures before opening up video server
        # OR just have a better secure handshake here

        self.startVideoConnection()
        return True


    def startVideoConnection(self, resolution=(128,128), udp=False):
        if (udp): # IF UDP
            stream = self.camera.getCircularBuffer()
            self.camera.startStream(stream)
            while True:
                self.camera.cameraObj.wait_recording(1)
                self.PRINT("stream done")
                self.PRINT(stream.readall())
        else:                # IF TCP
            self.PRINT("Waiting for video connection on port %s:%d" % (self.ip, self.video_port))
            self.videoServer.listen(1)
            (conn, (ip, port)) = self.videoServer.accept()
            self.PRINT("Video port connection established with %s" % ip)
            self.connectionEstablished = True
            self.clientConnection['running'] = True

            # BOTH COMMS AND VIDEO CONNECTIONS ESTABLISHED AT THIS POINT
            # GET FILE DESCRIPTOR OUT OF OUR CONNECTION SOCKET. WRITE VIDEO STREAM TO IT
            self.videoClient = conn
            self.videoClientFile = self.videoClient.makefile('wb')

            self.PRINT("Starting stream to %s" % ip)
            self.camera.startStream(self.videoClientFile)


    # Terminate and close everything related to both VIDEO and COMMS connections/sockets
    def terminateConnections(self):
        if (self.clientConnection['commsConn'] != None):
            self.clientConnection['commsConn'].close()
            self.clientConnection['commsConn'] = None
        if (VIDEO_OVER_UDP):
            pass # TODO VIDEO_OVER_UDP
        else:
            if (self.clientConnection['videoConn'] != None):
                self.clientConnection['videoConn'].close()
                self.clientConnection['videioConn'] = None
        self.clientConnection['running'] = False
        self.connectionEstablished = False
        self.PRINT('Connection with %s terminated' % self.clientConnection['ip'])

    # Process commands received from the COMMS_CONNECTION
    # Packet types defined in comms_packet_structure.py
    def processInput(self, data):
        inputType = data[0]
        self.PRINT("Data received: %s. input type: %d" % (bytearray(data), inputType))

        if (inputType == CommsPacketType.CMD_CAMERA_ANGLE_CHANGED.value):
            unpackedData = struct.unpack('BBB', data)[1:]
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
            self.PRINT("NEW X: %d, NEW Y: %d" % (newX, newY))

    # Main loop of the server program. The class itself doesnt jump to this function
    def run(self):
        self.running = True

        self.PRINT("Starting kitty server")

        # MAIN LOOP
        while self.running:
            self.initialize()
            if (not self.connectionSequence()):
                self.PRINT("[!] Connection sequence failed.")
                self.deinitialize() # TODO make this prettier. we dont heed to deinit every time conn sequence fails
                continue

            # Start comms threads
            self.serverRxThread.start()
            #self.serverTxThread.start()

            # Wait while we're connected to a client.
            while self.clientConnection:
                pass

            # When a disconnect occurs, deinitialize
            self.deinitialize()

            time.sleep(5)

        self.PRINT("Shutting down server")



def main():
    print("K i t t y S u r v e i l l a n c e - Server - v%s" % (VERSION))
    server = KittyServer(SERVER_IP_ADDR, VIDEO_IP_PORT, COMMS_IP_PORT)
    server.run()

if __name__ == '__main__':
    main()
