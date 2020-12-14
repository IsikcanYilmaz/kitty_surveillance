#!/usr/bin/env python3

from enum import Enum, auto
import struct

'''
COMMS Packets 
The communication protocol that this project uses. Aim is to be simple and extensible enough
for the purposes of this project. 

The basic structure looks like the following c structure
struct {
 uint8_t  header;
 uint16_t cmd_id;
 uint16_t payload_len;
 uint8_t  *payload;
 uint32_t magic_number;
}

MakeCommsPacket creates a bytes object from the parameters $cmd_id and an arbitrary payload.
DecodeRawCommsPacket creates a human readable dictionary from said bytes object. However the
payload part is still just bytes. Each command handler should know what to do with those bytes.

for my ease of doing socket.recv(), i make sure the size of the entire packet is a multiple of 
four. so i just do recv(4) over and over and i keep looking for the magic string. we'll see if 
this will work. 

thats kinda it tbh.
'''

COMMS_PACKET_HEADER = [0xff]
COMMS_PACKET_MAGIC  = [0x12, 0x34, 0x56, 0x78]

class CommsPacketType(Enum):
    CMD_START_RECORDING_VIDEO = 0
    RSP_START_RECORDING_VIDEO = 1
    CMD_STOP_RECORDING_VIDEO  = 2
    RSP_STOP_RECORDING_VIDEO  = 3
    CMD_INITIATE_VIDEO_SERVER = 4
    RSP_INITIATE_VIDEO_SERVER = 5
    CMD_CAMERA_ANGLE_CHANGED  = 6
    RSP_CAMERA_ANGLE_CHANGED  = 7

class CommsErrorType(Enum):
    COMMS_SUCCESS = 0
    COMMS_ERROR  = 1
    COMMS_BAD_PACKET = 2

def MakeCommsPacket(cmd_id, payload):
    # Payload size will be a factor of 4 always.
    while (len(payload) % 4 != 0):
        payload.append(0)
    rawPacket = [*COMMS_PACKET_HEADER, cmd_id, *struct.pack('>H', len(payload)), *payload, *COMMS_PACKET_MAGIC]
    return bytes(rawPacket)

def DecodeRawCommsPacket(rawPacket):
    error = CommsErrorType.COMMS_SUCCESS
    try:
        header, cmd_id, payloadLen = struct.unpack('>ccH', rawPacket[0:4])
        payload = rawPacket[4:4+payloadLen]
        magic = rawPacket[-len(COMMS_PACKET_MAGIC):]
        if (header != bytes(COMMS_PACKET_HEADER) or magic != bytes(COMMS_PACKET_MAGIC)):
            print("[!] Error in header or magic number of the packet header,magic " , header, [hex(i) for i in magic])
            error = CommsErrorType.COMMS_BAD_PACKET
    except Exception as e:
        print("[!] Error decoding packet", e)
        cmd_id = None
        payload = None
        error = CommsErrorType.COMMS_ERROR
    return {'cmd_id':struct.unpack('B', cmd_id)[0], 'payload':payload, 'error':error}

