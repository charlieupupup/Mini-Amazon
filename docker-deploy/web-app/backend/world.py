import base
import world_amazon_pb2
import IG1_pb2

HOST_WORLD = ''
PORT_WORLD = 23456

SIMSPEED = 100

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

    def init(self, world_id=0):
        """
        message AConnect{
            optional int64 worldid = 1;
            repeated AInitWarehouse initwh = 2;
            required bool isAmazon = 3;
            }

        """
        msg_init = world_amazon_pb2.AConnect()
        msg.worldid = world_id
        msg.initwh = self.init_warehouse()
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
        return res.worldid

    """
    normal
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

    def normal(self, raw_byte, seq=0):
        msg = world_amazon_pb2.AResponses()
        msg.ParseFromString(raw_byte)

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

        def put_on_truck(self, package, seq_num):
            command = world_amazon_pb2.ACommands()
            command.simspeed = SIMSPEED
            pack = command.load.add()
            pack.whnum = package.whnum
            pack.shipid = package.ship_id
            pack.truckid = package.truck_id
            pack.seq = seq_num

            # send the info
            self.send(command)

            # check for ack
            self.recv()

        def to_pack(self, product, seq_num, ship_id):
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

        def purchase(self, product):
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

        def world(self, msg):
            if (len(msg) > 0):
                response = world_amazon_pb2.AResponses()
                response.ParseFromString(msg)
                print(response)
                # handle import new stock
                for arrive in response.arrived:
                    things = arrive.things
                    for thing in things:
                        products = Whstock.objects.filter(pid=thing.id)
                        if len(products) != 0:
                            products[0].count = products[0].count + thing.count
                            products[0].save()
                        else:
                            # need to specify world id
                            whstock = Whstock()
                            whstock.hid = arrive.whnum
                            whstock.pid = thing.id
                            whstock.dsc = thing.description
                            whstock.count = thing.count
                            whstock.save()

                for currReady in response.ready:
                    # save current state
                    trans = Transaction.objects.get(ship_id=currReady)
                    trans.ready = True
                    trans.save()
                    # connect to UPS
                    ups_handler = threading.Thread(
                        target=self.process_Uresponse, args=(trans,))
                    ups_handler.start()
                    self.AUCommand(trans, 0)
                    print("first msg for UPS sent(to pickup)")
                    ups_handler.join()

                # load info from sim
                for load in response.loaded:
                    # save current state
                    trans = Transaction.objects.get(ship_id=load)
                    trans.loaded = True
                    trans.save()
                    # connect to UPS
                    self.AUCommand(trans, 1)
                    print("second msg for UPS sent(get load success from sim world)")
