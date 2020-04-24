from .base import Base
from . import world_amazon_pb2
from . import IG1_pb2

from stock.models import stock, product, warehouse
from order.models import order

import threading


class World(Base):
    """
    init
    """

    def setUPS(self, ups):
        self.ups = ups

    def init(self, world_id):
        """
        message AConnect{
            optional int64 worldid = 1;
            repeated AInitWarehouse initwh = 2;
            required bool isAmazon = 3;
            }

        """
        msg_init = world_amazon_pb2.AConnect()
        msg_init.worldid = world_id

        info_wh = warehouse.objects.all()

        for w in info_wh:
            curr_wh = msg_init.initwh.add()
            curr_wh.id = w.whid
            curr_wh.x = w.x
            curr_wh.y = w.y
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

        th_handler = threading.Thread(target=self.handler, args=())
        th_handler.setDaemon(True)
        th_handler.start()
    """
    handler
    """

    def handler(self):
        while True:
            raw_byte = self.recv()
            self.response(raw_byte)

    def header(self):
        command = world_amazon_pb2.ACommands()
        command.simspeed = self.simspeed
        return command

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

    def response(self, raw_byte):

        msg = world_amazon_pb2.AResponses()
        msg.ParseFromString(raw_byte)
        print("receive: ", msg)

        # parse info in msg
        self.res_arr(msg)
        self.res_rdy(msg)
        self.res_load(msg)
        self.res_err(msg)
        self.res_ack(msg)
        self.res_pkgsts(msg)

    def res_arr(self, msg):
        info_world = self.header()
        # arrived
        for arr in msg.arrived:
            # check proceed or not
            if arr.seqnum not in self.recv_msg:
                self.recv_msg.add(arr.seqnum)

                # warehouse num
                wh_num = arr.whnum

                # Aproduct
                for p in arr.things:
                    idx = p.id
                    des = p.description
                    cnt = p.count

                    curr_s = stock.objects.get(pid=idx, whid=wh_num)
                    curr_s.count += cnt
                    curr_s.save()

                info_world.acks.append(arr.seqnum)

        self.send(info_world)

    def res_rdy(self, msg):
        info_world = self.header()

        # repeated APacked ready
        for r in msg.ready:
            """
            message APacked {
            required int64 shipid = 1;
            required int64 seqnum = 2;
            }
            """
            if r.seqnum not in self.recv_msg:
                self.recv_msg.add(r.seqnum)
                # ship id
                ship_id = r.shipid
                shipment = order.objects.get(pkgid=ship_id)
                self.ups.sendTruck(shipment)

                # ack
                info_world.acks.append(r.seqnum)

        self.send(info_world)

    def res_load(self, msg):
        info_world = self.header()
        # repeated ALoaded loaded
        for l in msg.loaded:
            """
            message ALoaded{
            required int64 shipid = 1;
            required int64 seqnum = 2;
            }
            """
            if l.seqnum not in self.recv_msg:
                self.recv_msg.add(l.seqnum)
                sid = l.shipid
                seq = l.seqnum

                shipment = order.objects.get(pid=sid)
                self.ups.loaded(shipment)

                info_world.acks.append(seq)

        self.send(info_world)

    def res_ack(self, msg):
        # pop out seq
        for a in msg.acks:
            self.seq_dict.pop(a, None)

    """
    message AErr{
        required string err = 1;
        required int64 originseqnum = 2;
        required int64 seqnum = 3;
        }
    """

    def res_err(self, msg):
        info_world = self.header()
        for e in msg.error:
            print(e.err)
            if e.seqnum not in self.recv_msg:
                self.recv_msg.add(e.seqnum)
                info_world.acks.append(e.seqnum)

        self.send(info_world)

    def res_pkgsts(self, msg):
        info_world = self.header()
        # repeated APackage packagestatus = 7;
        for pkg in msg.packagestatus:
            """
            message APackage{
            required int64 packageid =1;
            required string status = 2;
            required int64 seqnum = 3;
            }
            """
            if pkg.seqnum not in self.recv_msg:
                self.recv_msg.add(pkg.seqnum)
                pkg_id = pkg.packageid
                s = pkg.status
                seq = pkg.seqnum

                curr_order = order.objects.get(pkgid=pkg_id)
                curr_order.status = s
                curr_order.save()

                info_world.acks.append(seq)

        self.send(info_world)

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

    def put_on_truck(self, curr_order):
        command = self.header()
        pack = command.load.add()

        pack.whnum = curr_order.whid
        pack.shipid = curr_order.pkgid
        pack.truckid = curr_order.truckid
        pack.seq = self.seq_num

        self.seq_dict[self.seq_num] = command
        self.seq_num += 1

        # send the info
        self.send(command)

    """
    message AQuery{
        required int64 packageid = 1;
        required int64 seqnum = 2;
        }
    """

    def query(self):
        command = self.header()

        orders = order.objects.all()

        for o in orders:

            q = command.queries.add()
            q.packageid = o.pkgid
            q.seqnum = self.seq_num
            self.seq_dict[self.seq_num] = command

            self.seq_num += 1

        self.send(command)

    """
    message APack{
        required int32 whnum = 1;
        repeated AProduct things = 2;
        required int64 shipid = 3;
        required int64 seqnum = 4;
        }
    """

    def pack(self, pkg_id):
        command = self.header()
        # filling info of topack
        # type: Apack
        pack = command.topack.add()

        curr_order = order.objects.get(pkgid=pkg_id)

        pack.whnum = curr_order.whid

        # fill things field
        p = pack.things.add()

        pro = product.objects.get(pid=curr_order.pid)
        p.id = pro.pid
        p.description = pro.description
        p.count = curr_order.count

        pack.shipid = pkg_id
        pack.seqnum = self.seq_num

        self.seq_dict[self.seq_num] = command
        self.seq_num += 1
        self.send(command)

    """
    message APurchaseMore{
        required int32 whnum = 1;
        repeated AProduct things = 2;
        required int64 seqnum = 3;
        }
    """

    def purchase_more(self, product_id, wh_num, count):
        command = self.header()
        # populate buy
        # type: APurchaseMore
        purchase = command.buy.add()
        purchase.whnum = wh_num

        # populate things
        # type: AProduct
        p = purchase.things.add()

        pro = product.objects.get(pid=product_id)
        p.id = product_id
        p.description = pro.description
        p.count = count

        purchase.seqnum = self.seq_num

        self.seq_dict[self.seq_num] = command
        self.seq_num += 1
        self.send(command)
