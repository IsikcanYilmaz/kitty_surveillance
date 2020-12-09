

from enum import Enum, auto

# Comms command packet structure definitions

class CommsPacketType(Enum):
    CMD_START_RECORDING_VIDEO = auto()
    CMD_STOP_RECORDING_VIDEO  = auto()
    CMD_INITIATE_VIDEO_SERVER = auto()
    CMD_CAMERA_ANGLE_CHANGED = auto()

class CommsPacket():
    def __init__(self, CommsPacketType):
        pass

