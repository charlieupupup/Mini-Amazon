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
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self, msg, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data_string = msg.SerializeToString()
            size = msg.ByteSize()
            s.sendall(_VarintBytes(size))
            s.sendall(data_string)

    def recv(self):
        # Brian
        var_int_buff = []

        while True:
            buf = world_socket.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break
        whole_message = world_socket.recv(msg_len)
        # int length is at most 4 bytes long
        hdr_bytes = self.sock.recv(4)
        (msg_length, hdr_length) = _DecodeVarint32(hdr_bytes, 0)
        rsp_buffer = io.BytesIO()
        if hdr_length < 4:
            rsp_buffer.write(hdr_bytes[hdr_length:])

        # read the remaining message bytes
        msg_length = msg_length - (4 - hdr_length)
        while msg_length > 0:
            rsp_bytes = self.sock.recv(min(8096, msg_length))
            rsp_buffer.write(rsp_bytes)
            msg_length = msg_length - len(rsp_bytes)

        return rsp_buffer.getvalue()
