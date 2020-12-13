#!/usr/bin/env python3

from enum import Enum, auto
import struct

# Comms command packet structure definitions

COMMS_PACKET_HEADER = [0xff]
COMMS_PACKET_MAGIC  = [0x12, 0x34, 0x56, 0x78]

class CommsPacketType(Enum):
    CMD_START_RECORDING_VIDEO = auto()
    CMD_STOP_RECORDING_VIDEO  = auto()
    CMD_INITIATE_VIDEO_SERVER = auto()
    CMD_CAMERA_ANGLE_CHANGED  = auto()
    CMD_MAX                   = 1024

def MakeCommsPacket(cmd_id, payload):
    rawPacket = [*COMMS_PACKET_HEADER, *struct.pack('>H', cmd_id), *struct.pack('>H', len(payload)), *payload, *COMMS_PACKET_MAGIC]
    return bytes(rawPacket)

def DecodeRawCommsPacket(rawPacket):
    error = 0
    try:
        header, cmd_id, payloadLen = struct.unpack('>cHH', rawPacket[0:5])
        payload = rawPacket[5:5+payloadLen]
        magic = rawPacket[-len(COMMS_PACKET_MAGIC):]
        if (header != bytes(COMMS_PACKET_HEADER) or magic != bytes(COMMS_PACKET_MAGIC)):
            print("[!] Error in header or magic number of the packet header,magic " , header, [hex(i ) for i in magic])
            error = 1
    except Exception as e:
        print("[!] Error decoding packet", e)
        cmd_id = None
        payload = None
        error = 1
    return {'cmd_id':cmd_id, 'payload':payload, 'error':error}

# test code
if __name__ == "__main__":
    a = MakeCommsPacket(CommsPacketType.CMD_CAMERA_ANGLE_CHANGED.value, [1,2,3,4,5,6,5,4,3,2])
    print([hex(i) for i in a])
    DecodeRawCommsPacket(a)


