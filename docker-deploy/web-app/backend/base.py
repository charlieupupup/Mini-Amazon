import socket
import io
#encode & decode
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

import IG1_pb2

import threading
"""
Base class for communication
mainly for encode & decode
"""


class Base():
    def send(self, msg, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data_string = msg.SerializeToString()
            size = msg.ByteSize()
            s.sendall(_VarintBytes(size))
            s.sendall(data_string)

    def recv(self, HOST, PORT, sock):
        all_data = b''
        data = sock.recv(4)
        if not data:
            print('error: cannot recv raw byte')
        data_len, new_pos = _DecodeVarint32(data, 0)
        all_data += data[new_pos:]

        data_left = data_len - len(all_data)
        while True:
            data = sock.recv(data_left)
            all_data += data
            data_left -= len(data)

            if data_left <= 0:
                break

        return all_data
