#!/usr/bin/python3

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = '127.0.0.1'
TCP_PORT = 9999
BUFFER_SIZE = 20

class ServerThread(Thread):
    def __init__(self, conn, ip, port):
        pass

    def run(self):
        pass


def main():
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((TCP_IP, TCP_PORT))

    while True:
        tcpServer.listen(1)
        (conn, (ip, port)) = tcpServer.accept()


if __name__ == '__main__':
    main()
