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

    def recv(self):
        # Brian
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as world_socket:
            var_int_buff = []

            while True:
                buf = world_socket.recv(1)
                var_int_buff += buf
                msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
                if new_pos != 0:
                    break
            whole_message = world_socket.recv(msg_len)
            return whole_message
