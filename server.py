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
from comms_packet_structure import *

BUFFER_SIZE = 20
BUFFER_FILENAME = 'buffer.h264'

class KittyServer():
    def __init__(self, ip, comms_port):
        self.ip = ip
        self.comms_port = comms_port
        self.running = False

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

        # ServerRxThread and TxThread for the communication of commands, coordinates, etc.
        self.serverRxThread = threading.Thread(target=self.ServerRxThread)
        self.serverTxThread = threading.Thread(target=self.ServerTxThread)

        self.connectionEstablished = False
        self.clientConnection = {}

        self.cameraX = 45
        self.cameraY = 45
        self.camera = None # TODO

        self.motors = Motors()

    # Joins threads, destroys camera and motor objects. Add anything else if you think of any
    def deinitialize(self):
        self.serverRxThread.join()
        self.serverTxThread.join()
        del(self.camera)
        del(self.motors)

    # This thread continuously receives data, passes to processInput
    # TODO: Currently there's one size in receiving. have this
    def ServerRxThread(self):
        self.PRINT("Server Rx thread started")
        rxBuf = []
        while (self.connectionEstablished):
            try:
                rxData = self.clientConnection['commsConn'].recv(4)
                rxBuf.extend(rxData)
                print([hex(i) for i in rxData], rxData == [], len(rxData))
                # If we received the magic number, we can assume we have 
                # a full packet in our hands. process it.
                if (rxData == bytes(COMMS_PACKET_MAGIC)):
                    self.processInput(rxBuf)
                    rxBuf = []
                if (rxData == None or rxData == [] or len(rxData) == 0):
                    print("[!] rxData == None. Terminating connection")
                    self.terminateConnections()
            except Exception as e:
                print("[!] ERROR!")
                print(e)
                print("[!] TERMINATING CONNECTION")
                self.terminateConnections()
        self.PRINT("Server Rx thread ending")


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
        self.connectionEstablished = True
        # TODO # add security measures before opening up video server
        # OR just have a better secure handshake here

        return True


    # Terminate and close everything related to both VIDEO and COMMS connections/sockets
    def terminateConnections(self):
        if (self.clientConnection['commsConn'] != None):
            self.clientConnection['commsConn'].close()
            self.clientConnection['commsConn'] = None

        self.clientConnection['running'] = False
        self.connectionEstablished = False
        self.PRINT('Connection with %s terminated' % self.clientConnection['ip'])

    # Process commands received from the COMMS_CONNECTION
    # Packet types defined in comms_packet_structure.py
    def processInput(self, data):
        decodedPacket = DecodeRawCommsPacket(bytes(data))
        print('[*] Processed packet: ', decodedPacket)
        if (decodedPacket['cmd_id'] == CommsPacketType.CMD_CAMERA_ANGLE_CHANGED.value):
            payload = decodedPacket['payload'][0:2] # rest of the bytes are padding bytes
            try:
                newX, newY = struct.unpack('BB', payload)
            except Exception as e:
                print(e)
                print(data)
                return
            
            print("[*] CAMERA ANGLE CHANGED.", newX, newY)

            if (newX < 0):
                newX = 0
            elif (newX > 180):
                newX = 180

            if (newY < 0):
                newY = 0
            elif (newY > 180):
                newY = 180

            self.motors.setX(newX)
            self.motors.setY(newY)
            self.PRINT("NEW X: %d, NEW Y: %d" % (newX, newY))

        if (decodedPacket['cmd_id'] == CommsPacketType.CMD_START_RECORDING_VIDEO.value):
            pass

        if (decodedPacket['cmd_id'] == CommsPacketType.CMD_STOP_RECORDING_VIDEO.value):
            pass

        if (decodedPacket['cmd_id'] == CommsPacketType.CMD_INITIATE_VIDEO_SERVER.value):
            pass

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
            #self.serverTxThread.start() # TODO # Eventually implement tx stuff

            # Wait while we're connected to a client.
            while self.clientConnection:
                pass

            # When a disconnect occurs, deinitialize
            self.deinitialize()

            time.sleep(5)

        self.PRINT("Shutting down server")



def main():
    print("K i t t y S u r v e i l l a n c e - Server - v%s" % (VERSION))
    server = KittyServer(SERVER_IP_ADDR, COMMS_IP_PORT)
    server.run()

if __name__ == '__main__':
    main()
