from .base import Base
from . import world_amazon_pb2
from . import IG1_pb2
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes
import threading

HOST_UPS = ''
PORT_UPS = 23456


class ComUPS(Base):

    def setWorld(self, world):
        self.world = world

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

    # Only use this method to receive from Amazon
# Return a Message object


def ARecv(sock):
    #    sock_lock.acquire()
    all_data = b''
    data = sock.recv(4)
    if not data:
        print('connection to amazomn is closed')
    data_len, new_pos = _DecodeVarint32(data, 0)
    all_data += data[new_pos:]

    data_left = data_len - len(all_data)
    while True:
        data = sock.recv(data_left)
        all_data += data
        data_left -= len(data)

        if data_left <= 0:
            break

    msg = uapb.ACommunicate()
    msg.ParseFromString(all_data)
    return msg

    # Process AResponse


def ProcessARes(msg, aSock, wSock, conn):
    print('process aresponse')
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
