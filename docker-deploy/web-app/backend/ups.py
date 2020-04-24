from .base import Base
from . import world_amazon_pb2
from . import IG1_pb2
from stock.models import stock, warehouse, product
from order.models import order

import threading


class UPS(Base):

    # init: set world id & tell world
    # message UInitialWorld{
    #         required int64 worldid = 1;
    #         required int64 seq = 2;
    # }
    def init(self):
        msg = self.receive()
        # send back
        msg_init = IG1_pb2.AMsg()
        msg_init.acks.append(msg.initworld.seq)
        print(msg_init)
        self.send(msg_init)
        # tell world
        self.world.init(msg.initworld.worldid)
        # start processing response
        responseHandler = threading.Thread(target=self.processResponse)
        responseHandler.setDaemon(True)
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
        # seq
        self.seq_num += 1
        temp = self.seq_num
        truck.seq = temp
        self.seq_dict[temp] = msg
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
        # seq
        self.seq_num += 1
        temp = self.seq_num
        loaded.seq = temp
        self.seq_dict[temp] = msg
        # send
        self.send(msg)

    # order placed
    # message UOrderPlaced{
    #             required int64 pkgid = 1; // Package ID
    #             required int32 truckid = 2; // Truck ID
    #             required int64 seq = 3; //Sequence number
    # }
    def orderPlaced(self, placed):
        print('orderPlaced')
        UPSOrder = order.objects.get(pkgid=placed.pkgid)
        # update order
        UPSOrder.truckid = placed.truckid
        UPSOrder.save()
        return placed.seq

    # truck arrived & tell world to load
    # message UTruckArrived{
    #             required int32 truckid = 1; //Truck ID
    #             required int64 seq = 2; //Sequence number
    # }
    def truckArrived(self, arrived):
        print('truckArrived')
        UPSOrder = order.objects.get(truckid=arrived.truckid)
        # tell world
        self.world.put_on_truck(UPSOrder)
        return arrived.seq

    # package delivered
    # message UPkgDelivered{
    #             required int64 pkgid = 1;
    #             required int64 seq = 2;
    # }
    def pkgDelivered(self, delivered):
        print('pkgDelivered')
        # UPSOrder = order.objects.get(pkgid=delivered.pkgid)
        # # change status
        # UPSOrder.status = "delivered"
        # UPSOrder.save()
        return delivered.seq

    # Process Response
    # message UMsg{
    #         repeated UOrderPlaced uorderplaced = 1;                            (optional)
    #         repeated UTruckArrived utruckarrived = 2; // Truck arrived at the warehouse          (optional)
    #         repeated UPkgDelivered udelivered = 3; // Package delivered             (optional)
    #         optional UInitialWorld initworld = 4
    #         repeated int64 acks = 5;                                        (optional)
    # }
    def processResponse(self):
        print('processing response')
        while True:
            msg = self.receive()
            back = IG1_pb2.AMsg()
            for placed in msg.uorderplaced:
                if placed.seq not in self.recv_msg:
                    self.recv_msg.add(placed.seq)
                    back.acks.append(self.orderPlaced(placed))
            for arrived in msg.utruckarrived:
                if arrived.seq not in self.recv_msg:
                    self.recv_msg.add(arrived.seq)
                    back.acks.append(self.truckArrived(arrived))
            for delivered in msg.udelivered:
                if delivered.seq not in self.recv_msg:
                    self.recv_msg.add(delivered.seq)
                    back.acks.append(self.pkgDelivered(delivered))
            for ack in msg.acks:
                self.seq_dict.pop(ack, None)
            # send back
            self.send(back)
