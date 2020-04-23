from .base import Base
import world_amazon_pb2
import IG1_pb2

HOST_WORLD = ''
PORT_WORLD = 23456

SIMSPEED = 100

"""
world
"""

# normal communication


class ComWorld(Base):
    # set ups
    def setUPS(self, ups):
        self.ups = ups
    # init
    def init(self, raw_byte):
        msg = world_amazon_pb2.AConnected()
        msg.ParseFromString(raw_byte)
        return msg

    # normal communication
    def normal(self, raw_byte):
        msg = world_amazon_pb2.AResponses()
        msg.ParseFromString(raw_byte)
        return msg

    # get world id
    def init_world(self, world_id):
        msg = world_amazon_pb2.AConnect()
        msg.isAmazon = True

        # todo: diff of world id
        if world_id == 0:
            # init warehouse
            self.init_warehouse()

        if world_id > 0:
            msg.worldid = world_id

        self.send(msg)

        # wait for response
        raw_byte = self.recv()
        info = self.init(raw_byte)
        print(info)
        return info.worldid

    def init_warehouse(self):
        return

    def ProcessURes(msg, wSock, aSock, db):
        print('Process UResponse...')
        print(msg)
        global SeqNum
        toAmazonEmpty = True
        toWorldEmpty = True

        # Prepare UCommand & UCommunicate
        ToWorld = wupb.UCommands()
        ToAmazon = uapb.UCommunicate()

        # check for UFinished
        print('Looking into UFinished msg')
        for ufin in msg.completions:
            toWorldEmpty = False

            # Add ACK
            ToWorld.acks.append(ufin.seqnum)

            # Check ufinished status, notify amazon
            # first check whether this ufin has been processed before
            entry = Wrecvseq(db, ufin.seqnum)
            if entry:
                continue

            # record the seqnum from World
            Insertwrecv(db, ufin.seqnum)

            if ufin.status == 'ARRIVE WAREHOUSE':
                toAmazonEmpty = False
                print('notify amazon')
                arrive = ToAmazon.uarrived.add()
                arrive.truckid = ufin.truckid
                with seq_lock:
                    arrive.seqnum = SeqNum
                    SeqNum += 1
                Insertusend(db, arrive.seqnum,
                            arrive.SerializeToString(), 'UArrivedAtWarehouse')
                Truckstatus(db, ufin.truckid, 'loading')

            elif ufin.status == 'IDLE':
                print('dont need notify, notify in delivered')
                # update truck status in database to idle
                Truckstatus(db, ufin.truckid, 'idle')

        # check for UDeliveryMade
        print('Looking into UDeliveryMade Msg...')
        for udel in msg.delivered:
            toWorldEmpty = False
            toAmazonEmpty = False

            # Add ACK
            ToWorld.acks.append(udel.seqnum)

            #  first check whether this udel has been processed before
            if Checkdelivered(db, udel.packageid):
                continue

            # send out notification email
            SendEmail(db, udel.packageid)

            # record the seqnum from World
            Insertwrecv(db, udel.seqnum)

            # update delivery status for package in db, send to amazon
            delivered = ToAmazon.udelivered.add()
            delivered.packageid = udel.packageid
            Packagestatus(db, udel.packageid, 'delivered')
            Truckamount(db, udel.truckid, False)

            # record this MSG in database
            with seq_lock:
                delivered.seqnum = SeqNum
                Insertusend(db, SeqNum, delivered.SerializeToString(),
                            'UPackageDelivered')
                SeqNum += 1

        # add ack for truckstatus, if any
        for utruck in msg.truckstatus:
            toWorldEmpty = False
            # Add ACK
            ToWorld.acks.append(utruck.seqnum)
            UpdatePackagePos(db, utruck.truckid, utruck.x, utruck.y)

        # Check the acks field, delete those in UPS seqnum table
        for ACK in msg.acks:
            Deleteusend(db, ACK)

        # Send ACK to World & updates to Amazon
        if not toWorldEmpty:
            Send(wSock, ToWorld)
        if not toAmazonEmpty:
            Send(aSock, ToAmazon)

    # Resend msg whose ACK is missing

    def PacketDrop(wSock, aSock, db):
        print('check seqnum table every 30s, resend all those request/ACK')

        while True:
            time.sleep(30)
            print('start to check ack')
            with db_lock:
                cur = db.cursor()
                sql = 'SELECT * FROM usend'
                cur.execute(sql)
                row = cur.fetchone()

            ToWorld = wupb.UCommands()
            ToAmazon = uapb.UCommunicate()
            ToWorld_empty = True
            ToAmazon_empty = True

            while row:
                with db_lock:
                    # TOCHECK: distinguish what type of Msg, add to ToWorld or ToAmazon
                    if row[2] == 'UGoPickup':
                        print('resend UGoPickup')
                        tp = ToWorld.pickups.add()
                        ToWorld_empty = False
                    elif row[2] == 'UGoDeliver':
                        print('resend UGoDeliver')
                        tp = ToWorld.deliveries.add()
                        ToWorld_empty = False
                    elif row[2] == 'UQuery':
                        print('resend UQuery')
                        tp = ToWorld.queries.add()
                        ToWorld_empty = False
                    elif row[2] == 'UOrderPlaced':
                        print('resend UOrderPlaced')
                        tp = ToAmazon.uorderplaced.add()
                        ToAmazon_empty = False
                    elif row[2] == 'UArrivedAtWarehouse':
                        print('resend UArrivedAtwarehouse')
                        tp = ToAmazon.uarrived.add()
                        ToAmazon_empty = False
                    elif row[2] == 'UPackageDelivered':
                        print('resend UPackageDelivered')
                        tp = ToAmazon.udelivered.add()
                        ToAmazon_empty = False

                    tp.ParseFromString(row[1])
                    row = cur.fetchone()

            if not ToWorld_empty:
                Send(wSock, ToWorld)
            else:
                print('world empty')
            if not ToAmazon_empty:
                Send(aSock, ToAmazon)
            else:
                print('amazon empty')

        def world_put_on_truck(self, package, seq_num, HOST_WORLD, PORT_WORLD):
            command = world_amazon_pb2.ACommands()
            command.simspeed = SIMSPEED
            pack = command.load.add()
            pack.whnum = package.whnum
            pack.shipid = package.ship_id
            pack.truckid = package.truck_id
            pack.seq = seq_num

            # send the info
            self.send(command, HOST_WORLD, PORT_WORLD)

            # check for ack
            self.recv(HOST_WORLD, PORT_WORLD)

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
                # handle pack ready response
                # when ready send AU command to let UPS truck pickup,
                # use another thread for wait for UPS response
                # when receive response send ALoad command
                # when reveived loaded for Sim send AU command and let flag = 1;
                # tell UPS packages is ready and ask for trucks (provide destinaiton address)
                # tell warehouse to load when UPS trucks ready
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
