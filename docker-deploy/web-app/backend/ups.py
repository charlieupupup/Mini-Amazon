import base
import world_amazon_pb2
import IG1_pb2


"""
send request to ups
"""


class UPS(Base):
    """
    send
    """

    def ups(self, trans, flag, HOST_UPS, PORT_UPS):
        command = IG1_pb2.IG1()

        self.send(command, HOST_UPS, PORT_UPS)

    """
    seq & ack
    """

    """
    info from ups
    """

    def parse(self, info, trans):

        if (len(info) > 0):
            response = IG1_pb2.IG1()
            response.ParseFromString(info)
            print(response)
            if (response != None):
                self.ALoad(trans.ship_id, response.truckid)
                trans.package_id = response.packageid
                trans.save()
                return
