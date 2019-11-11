#!/usr/bin/python3
import socket
import subprocess

TCP_IP = '192.168.1.100'
#TCP_IP = '127.0.0.1'
TCP_PORT = 9998

class VideoClient:
    def __init__(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def streamTest(self, vlc=False):
        self.tcpClient.connect((TCP_IP, TCP_PORT))
        cmdline = ['vlc', '--demux', 'h264', '-']
        if (vlc):
            player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        else:
            f = open("teststream", "wb")
        buf = []
        while True:
            data = self.tcpClient.recv(1024)
            if not data:
                break
            else:
                print(data)
                if (vlc):
                    player.stdin.write(data)
                else:
                    f.write(data)
        if (not vlc):
            f.close()


def main():
    vidCli = VideoClient()
    vidCli.streamTest(vlc=True)
    pass

if __name__ == "__main__":
    main()

