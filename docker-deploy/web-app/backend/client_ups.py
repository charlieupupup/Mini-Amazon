import base
import world_amazon_pb2
import IG1_pb2
HOST_UPS = ''
PORT_UPS = 33333


"""
send request to ups
"""


class ClientUPS(Base):
    """
    ups
    """

    def ups(self, trans, flag):
        command = IG1_pb2.IG1()

        self.send(command, HOST_UPS, PORT_UPS)
