import base
import world_amazon_pb2
import IG1_pb2
HOST_UPS = ''
PORT_UPS = 33333

HOST_WORLD = ''
PORT_WORLD = 23456

SIMSPEED = 100

"""
send request to ups
"""


class Client(Base):
    """
    ups
    """

    def ups(self, trans, flag):
        command = IG1_pb2.IG1()

        self.send(command, HOST_UPS, PORT_UPS)

    """
    world
    """

    def world_put_on_truck(self, package, seq_num):
        command = world_amazon_pb2.ACommands()
        command.simspeed = SIMSPEED
        pack = command.load.add()
        pack.whnum = package.whnum
        pack.shipid = package.ship_id
        pack.truckid = package.truck_id
        pack.seq = seq_num

        # send the info
        self.send(command, HOST_WORLD, PORT_WORLD)

    def world_to_pack(self, product, seq_num, ship_id):
        command = world_amazon_pb2.ACommands()
        command.simspeed = SIMSPEED
        # filling info of topack
        # type: Apack
        pack = command.topack.add()

        pack.whnum = 0

        # fill things field
        p = pack.things.add()
        p.id = product.product_id
        p.description = product.description
        p.count = product.quantity

        pack.shipid = ship_id
        pack.seqnum = seq_num
        self.send(command, HOST_WORLD, PORT_WORLD)

    def world_purchase(self, product):
        command = world_amazon_pb2.ACommands()
        command.simspeed = SIMSPEED

        # populate buy
        # type: APurchaseMore
        purchase = command.buy.add()
        purchase.whnum = 0

        # populate things
        # type: AProduct
        p = purchase.things.add()
        p.id = product.product_id
        p.description = product.description
        p.count = product.quantity
        self.send(command, HOST_WORLD, PORT_WORLD)
