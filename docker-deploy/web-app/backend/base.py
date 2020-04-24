import socket
import io
import time
import threading
#encode & decode
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.encoder import _EncodeVarint

"""
Base class for communication
mainly for encode & decode
"""


class Base():
    def __init__(self, host, port, simspeed=100):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.simspeed = simspeed
        self.seq_num = 0
        self.seq_dict = dict()
        self.recv_msg = set()

        th_resend = threading.Thread(target=self.resend, args=())
        th_resend.setDaemon(True)
        th_resend.start()

    def __del__(self):
        self.socket.close()

    def send(self, msg):
        print("send: " + str(msg))
        if str(msg) != "":
            data_string = msg.SerializeToString()
            _EncodeVarint(self.socket.send, len(data_string), None)
            self.socket.send(data_string)

    def recv(self):
        var_int_buff = []
        while True:
            buf = self.socket.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break
        whole_message = self.socket.recv(msg_len)
        return whole_message

    # resend the seq num in seq_dict
    def resend(self):
        while True:
            time.sleep(10)
            for k in self.seq_dict:
                self.send(self.seq_dict[k])
