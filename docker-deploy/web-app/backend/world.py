from .base import Base
from . import world_amazon_pb2
from . import IG1_pb2

from ..stock.models import stock, product
from ..order.models import order


"""
world
"""


class World(Base):
    """
    init
    """
    # init warehouse

    def init_warehouse(self):
        pass

    def setUPS(self, ups):
        self.ups = ups

    def init(self, world_id=0):
        """
        message AConnect{
            optional int64 worldid = 1;
            repeated AInitWarehouse initwh = 2;
            required bool isAmazon = 3;
            }

        """
        msg_init = world_amazon_pb2.AConnect()
        msg_init.worldid = world_id
        msg_init.initwh = self.init_warehouse()
        msg_init.isAmazon = True

        self.send(msg_init)

        # wait for response
        """
        message AConnected{
            required int64 worldid= 1;
            required string result = 2;
            }
        """
        raw_byte = self.recv()
        res = world_amazon_pb2.AConnected()
        res.ParseFromString(raw_byte)
        print(res.result)
        assert world_id == res.worldid

        ups_handler = threading.Thread(
            target=self.process_Uresponse, args=(trans,))

    """
    handler
    """

    """
    message AResponses {
        repeated APurchaseMore arrived = 1;
        repeated APacked ready = 2; 
        repeated ALoaded loaded = 3; 
        optional bool finished = 4;
        repeated AErr error = 5;
        repeated int64 acks = 6;
        repeated APackage packagestatus = 7;
        }
    """

    def handler(self, raw_byte, dict):
        msg = world_amazon_pb2.AResponses()
        msg.ParseFromString(raw_byte)

        whstock = Whstock()

        whstock.save()

        # possible info send to world & ups
        info_world = world_amazon_pb2.ACommands()
        info_ups = IG1_pb2.AMsg()

        # parse info in msg
        # arrived
        for arr in msg.arrived:
            # warehouse num
            wh_num = arr.whnum

            # Aproduct
            for p in arr.things:
                idx = p.id
                des = p.description
                cnt = p.count

            # ack
            info_world.acks.append(arr.seqnum)

        self.send(info_world)

        # repeated APacked ready
        for r in msg.ready:
            """
            message APacked {
            required int64 shipid = 1;
            required int64 seqnum = 2;
            }
            """
            # ship id
            ship_id = r.shipid

            # ack
            info_world.acks.append(r.seqnum)

        # repeated ALoaded loaded
        for l in msg.loaded:
            """
            message ALoaded{
            required int64 shipid = 1;
            required int64 seqnum = 2;
            }
            """
            sid = l.shipid
            seq = l.seqnum

        # repeated int64 acks
        for a in msg.acks:
            dict.pop(a, None)

        # repeated APackage packagestatus = 7;
        for pkg in msg.packagestatus:
            """
            message APackage{
            required int64 packageid =1;
            required string status = 2;
            required int64 seqnum = 3;
            }
            """
            pkg_id = pkg.packageid
            s = pkg.status
            seq = pkg.seqnum

        """
        command
        """

        """
        message APutOnTruck{
            required int32 whnum = 1;
            required int32 truckid = 2;
            required int64 shipid = 3;
            required int64 seqnum = 4;
            }
        """

        def put_on_truck(self, package, seq_num):

            command = world_amazon_pb2.ACommands()
            command.simspeed = self.simspeed
            pack = command.load.add()
            pack.whnum = package.whnum
            pack.shipid = package.ship_id
            pack.truckid = package.truck_id
            pack.seq = seq_num

            # send the info
            self.send(command)

        """
        message APack{
            required int32 whnum = 1;
            repeated AProduct things = 2;
            required int64 shipid = 3;
            required int64 seqnum = 4;
            }
        """

        def pack(self, order_id, seq_num):
            command = world_amazon_pb2.ACommands()
            command.simspeed = self.simspeed
            # filling info of topack
            # type: Apack
            pack = command.topack.add()

            curr_order = order.objects.filter()

            pack.whnum = curr_order.whid

            # fill things field
            p = pack.things.add()

            product = product.objects.filter(pid=curr_order.pid)
            p.id = curr_order.pid
            p.description = product.description
            p.count = product.quantity

            pack.shipid = ship_id
            pack.seqnum = seq_num
            self.send(command)

        """
        message APurchaseMore{
            required int32 whnum = 1;
            repeated AProduct things = 2;
            required int64 seqnum = 3;
            }
        """

        def purchase_more(self, product_id, wh_num, seq_num):
            command = world_amazon_pb2.ACommands()
            command.simspeed = self.simspeed

            # populate buy
            # type: APurchaseMore
            purchase = command.buy.add()
            purchase.whnum = wh_num

            # populate things
            # type: AProduct
            p = purchase.things.add()

            product = stock.objects.filter(pid=product_id)
            p.id = product.product_id
            p.description = product.description
            p.count = product.quantity

            purchase.seqnum = seq_num
            self.send(command)
