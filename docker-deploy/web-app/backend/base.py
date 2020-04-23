import socket
import io
#encode & decode
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

"""
Base class for communication
mainly for encode & decode
"""


class Base():
    def __init__(self, host, port, simspeed):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.simspeed = simspeed

    def __del__(self):
        self.socket.close()

    def send(self, msg):
        data_string = msg.SerializeToString()
        size = msg.ByteSize()
        self.socket.sendall(_VarintBytes(size))
        self.socket.sendall(data_string)

    def recv(self):
        all_data = b''
        data = self.socket.recv(4)
        if not data:
            print('error: cannot recv raw byte')
        data_len, new_pos = _DecodeVarint32(data, 0)
        all_data += data[new_pos:]

        data_left = data_len - len(all_data)
        while True:
            data = self.socket.recv(data_left)
            all_data += data
            data_left -= len(data)

            if data_left <= 0:
                break

        return all_data
