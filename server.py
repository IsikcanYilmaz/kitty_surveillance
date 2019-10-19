#!/usr/bin/python3

import socket
import struct
from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 8888
BUFFER_SIZE = 20

class ServerThread(Thread):
    def __init__(self, conn, ip, port):
        pass

    def run(self):
        pass


def main():
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.bind((TCP_IP, TCP_PORT))

    while True:
        tcpServer.listen(1)
        (conn, (ip, port)) = tcpServer.accept()
        while True:
            data = bytes(conn.recv(4))
            if not data:
                break
            print(data)
            print("from connected user: ")
            print("length:", len(data))
            print(struct.unpack('I', data))


if __name__ == '__main__':
    main()
