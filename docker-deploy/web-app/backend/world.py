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

    def world(self):
        """
        world
        """
        while (True):
            str = self.recv(self.sock)
            if (len(str) > 0):
                response = world_amazon_pb2.AResponses()
                response.ParseFromString(str)
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
