#!/usr/bin/python3 

import subprocess

class ProcessManager:
    def __init__(self):
        pass

def EXT_runRaspicam(filename="vid", width=512, height=512, time_ms=12000):
    cmdStr = "raspivid -o /home/pi/kitty_surveillance_media/%s.h264 -w %s -h %s -t %s" % (filename, str(width), str(height), str(time_ms))
    p = subprocess.Popen(cmdStr.split(" "))
    return 0


# unit test code
if __name__ == "__init__":
    pass
