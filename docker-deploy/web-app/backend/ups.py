from .base import Base
from . import world_amazon_pb2
from . import IG1_pb2
from stock.models import stock, warehouse, product
from order.models import order

import threading

class UPS(Base):

    # init: set world id & tell world
    def init(self):
        self.seq = 0
        msg = self.receive()
        # send back
        msg_init = IG1_pb2.AMsg()
        msg_init.acks.append(msg.initworld.seq)
        self.send(msg_init)
        # tell world
        self.world.init(msg.initworld.worldid)
        # start processing response
        responseHandler = threading.Thread(target=self.processResponse)
        responseHandler.start()

    # set world object
    def setWorld(self, world):
        self.world = world

    # receive UMsg and parse
    # message UMsg{
    #             repeated UOrderPlaced uorderplaced = 1;
    #             repeated UTruckArrived utruckarrived = 2; // Truck arrived at the warehouse
    #             repeated UPkgDelivered upkgdelivered = 3; // Package delivered
    #             optional UInitialWorld initworld = 4;
    #             repeated int64 acks = 5;
    # }
    def receive(self):
        msg = IG1_pb2.UMsg()
        raw_byte = self.recv()
        msg.ParseFromString(raw_byte)
        print(msg)
        return msg

    # sendTruck
    # message AMsg{
    #             repeated ASendTruck asendtruck = 1;
    #             repeated AFinishLoading afinishloading = 2;
    #             repeated int64 acks = 3;
    # }
    # message ASendTruck{
    #         required WarehouseInfo whinfo = 1;
    #         required int32 x = 2;   // Buyer coordinate                  (must)
    #         required int32 y = 3;    // Buyer coordinate                 (must)
    #         required int64 pkgid = 4; // Package ID                    (must)
    #         repeated Product products = 5; // The products in a package             (optional)
    #         optional string upsid = 6;
    #         required int64 seq = 7; // Sequence number            (must)
    # }
    #
    # message WarehouseInfo{
    #         required int32 whid = 1; //The warehouse ID
    #         required int32 x = 2;      // x coordinate of wh
    #         required int32 y = 3;      // y coordinate of wh
    # }
    #
    # message Product{
    #         required int64 id = 1; //Product ID                             (must)
    #         required string description = 2; //Product description                  (must)
    #         required int32 count = 3; // Number of product          (must)
    # }
    def sendTruck(self, worldOrder):
        print('sendTruck')
        msg = IG1_pb2.AMsg()
        truck = msg.asendtruck.add()
        # whinfo
        truck.whinfo.whid = worldOrder.whid
        wh = warehouse.objects.get(whid=worldOrder.whid)
        truck.whinfo.x = wh.x
        truck.whinfo.y = wh.y
        #
        truck.x = worldOrder.whid
        truck.y = worldOrder.y
        truck.pkgid = worldOrder.pkgid
        # product
        products = truck.products.add()
        products.id = worldOrder.pid
        pd = product.objects.get(pid=worldOrder.pid)
        products.description = pd.description
        products.count = worldOrder.count
        #
        self.seq += 1
        truck.seq = self.seq
        # send
        self.send(msg)

    # loaded
    # message AMsg{
    #         repeated ASendTruck asendtruck = 1;                                  (optional)
    #         repeated AFinishLoading afinishloading = 2;                         (optional)
    #         repeated int64 acks = 3;                                                          (optional)
    # }
    # message AFinishLoading{
    #         required int64 pkgid = 1; //Package ID                      (must)
    #         required int32 truckid = 2; //Truck ID                         (must)
    #         required int64 seq = 3; //Sequence number              (must)
    # }
    def loaded(self, worldOrder):
        print('loaded')
        msg = IG1_pb2.AMsg()
        loaded = msg.afinishloading.add()
        loaded.pkgid = worldOrder.pkgid
        loaded.truckid = worldOrder.truckid
        self.seq += 1
        loaded.seq = self.seq
        # send
        self.send(msg)

    # truck arrived & tell world to load
    def truckArrived(self, truckId):
        worldOrder = order.objects.get(truckid=truckId)
        # update database
        worldOrder.arrived = True
        # tell world
        self.world.load(worldOrder)








    # Process AResponse
    def processResponse(self):
        print('processing response')
        print(msg)
        global SeqNum
        toWorldEmpty = True
        toAmazonEmpty = True

        # Check the acks field, delete those in UPS seqnum table
        for ack in msg.acks:
            Deleteusend(conn, ack)

        # Prepare UCommand & UCommunicate
        ToWorld = wupb.UCommands()
        ToAmazon = uapb.UCommunicate()

        # Check for AOrderPlaced
        for aor in msg.aorderplaced:
            print('process AOrderPlace')

            # Select one truck from truck table
            truck = Findidle(conn)
            if truck == -1:
                truck = Findtruck(conn)
                if truck == -1:
                    print('no truck available, ignore the order')
                    continue

            # Store in amazon seqnum table
            exists = Arecvseq(conn, aor.seqnum)
            if not exists:
                Insertarecv(conn, aor.seqnum)
            else:
                print('process before')
                continue

            toWorldEmpty = False
            toAmazonEmpty = False

            # Add ACK
            ToAmazon.acks.append(aor.seqnum)

            # Add package in package table
            items = ''
            amount = 0
            for thing in aor.things:
                if not items:
                    items = thing.name
                else:
                    items = items + ',' + thing.name
                amount += thing.count
            Insertpackage(conn, aor.packageid, aor.x, aor.y,
                          'created', items, amount, truck, aor.UPSuserid)

            # Add UGoPickup to ToWorld
            pick = ToWorld.pickups.add()
            pick.truckid = truck
            pick.whid = aor.whid
            with seq_lock:
                pick.seqnum = SeqNum
                SeqNum += 1

            # Add UOrderplaced to toAmazon
            order = ToAmazon.uorderplaced.add()
            order.packageid = aor.packageid
            order.truckid = truck
            with seq_lock:
                order.seqnum = SeqNum
                SeqNum += 1

            # Add send message to usend table
            Insertusend(conn, pick.seqnum, pick.SerializeToString(), 'UGoPickup')
            Insertusend(conn, order.seqnum,
                        order.SerializeToString(), 'UOrderPlaced')

            # Update status of package and truck
            Truckstatus(conn, truck, 'to warehouse')
            Packagestatus(conn, aor.packageid, 'truck en-route to warehouse')

        # Check for ALoadingFinished
        for alod in msg.aloaded:
            toWorldEmpty = False
            toAmazonEmpty = False
            print('process ALoadingFinished')

            # Store in amazon seqnum table
            exists = Arecvseq(conn, alod.seqnum)
            if not exists:
                Insertarecv(conn, alod.seqnum)
            else:
                print('process before')
                continue

            # Add ACK
            ToAmazon.acks.append(alod.seqnum)

            # Update status of package & update the truck amount
            Packagestatus(conn, alod.packageid, 'out for delivery')
            Truckamount(conn, alod.truckid, True)
            Truckstatus(conn, alod.truckid, 'delivering')

            # Add UGoDeliver to ToWorld
            xy = Packageaddress(conn, alod.packageid)
            deliver = ToWorld.deliveries.add()
            deliver.truckid = alod.truckid
            package = deliver.packages.add()
            package.packageid = alod.packageid
            package.x = xy[0]
            package.y = xy[1]
            with seq_lock:
                deliver.seqnum = SeqNum
                SeqNum += 1

            # Add send message to usend table
            Insertusend(conn, deliver.seqnum,
                        deliver.SerializeToString(), 'UGoDeliver')

        # Send ACK to World & Amazon
        if not toAmazonEmpty:
            Send(aSock, ToAmazon)
        if not toWorldEmpty:
            Send(wSock, ToWorld)
