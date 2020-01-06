

from enum import Enum, auto

# Comms command packet structure definitions

class CommsPacketType(Enum):
    CMD_INITIATE_VIDEO_SERVER = auto()
    CMD_CAMERA_ANGLE_CHANGED = auto()
