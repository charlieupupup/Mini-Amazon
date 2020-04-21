import base
import world_amazon_pb2


HOST_UPS = ''
PORT_UPS = 12345

"""
send request to ups
"""


class Client(Base):
    """
    proceed the amazon command
    """

    def AConnect(self):
        msg = amazon_pb2.AConnect()
        msg.worldid = 1000
        self.send(msg)
        self.recv()

    def process_AResponse(self):
        """
         process response of Acommnads, store the information in database for future reference
        """

        while (1):
            str = self.recv()
            if (len(str) > 0):
                response = amazon_pb2.AResponses()
                try:
                    response.ParseFromString(str)
                    print(response)
                    print(len(str))
                except:
                    print("error")

    def ALoad(self, ship_id, truck_id):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.load.add()
        pack.whnum = 0
        pack.shipid = ship_id
        pack.truckid = truck_id

        self.send(command)

    def AToPack(self, product_id, description, quantity, ship_id):
        """
        ship_id should be unique per ship
        """
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.topack.add()
        pack.whnum = 0
        pack.shipid = ship_id
        pid = pack.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command)

    def APurchase(self, product_id, description, quantity):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        purchase = command.buy.add()
        purchase.whnum = 0
        pid = purchase.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command)
