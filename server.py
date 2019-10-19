#!/usr/bin/python3

import socket
import struct
import threading

#TODO : need to redo following code
from set_pwm import *

#TCP_IP = '127.0.0.1'
TCP_IP = '192.168.1.109'
TCP_PORT = 9999
BUFFER_SIZE = 20

class KittyServer():
    def __init__(self, ip, port):
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.bind((ip, port))
        self.serverThread = threading.Thread(target=self.ServerThread)
        self.cameraX = 45
        self.cameraY = 45

    def receiveInput(self, data):
        unpackedData = struct.unpack('II', data)
        newX = unpackedData[0]
        newY = unpackedData[1]
        set_pwm(newX, newY)
        print("NEW X: %d, NEW Y: %d" % (newX, newY))

    def ServerThread(self):
        self.running = True
        while self.running:
            print("[+] Waiting for connection")
            self.tcpServer.listen(1)
            (conn, (ip, port)) = self.tcpServer.accept()
            print("[+] Connection established with %s:%d" % (ip, port))
            while True:
                try:
                    data = conn.recv(8)
                    if not data:
                        break
                    self.receiveInput(data)
                except Exception as e:
                    print("[!] Error")
                    print(e)

    def startServerThread(self):
        self.serverThread.start()



def main():
    server = KittyServer(TCP_IP, TCP_PORT)
    server.startServerThread()

if __name__ == '__main__':
    main()
