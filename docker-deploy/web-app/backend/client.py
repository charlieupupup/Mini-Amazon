import base
import world_amazon_pb2
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
    proceed the amazon command
    """

    def AUCommand(self, trans, flag):
        command = AU_pb2.AU()
        command.flag = flag
        command.shipid = trans.ship_id
        command.whid = trans.stock.hid
        command.detailofpackage = trans.product_name + \
            ":" + str(trans.product_num)
        if trans.package_id is not -1:
            command.packageid = trans.package_id
        command.x = trans.address_x
        command.y = trans.address_y
        if trans.ups_act is not None:
            command.ups_id = trans.ups_act
        self.send(command, self.Usock)

    def process_AResponse(self):
        """
        save data into db
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

    def A_put_on_truck(self, package, seq_num):
        command = world_amazon_pb2.ACommands()
        command.simspeed = SIMSPEED
        pack = command.load.add()
        pack.whnum = package.whnum
        pack.shipid = package.ship_id
        pack.truckid = package.truck_id
        pack.seq = seq_num

        # send the info
        self.send(command, HOST_WORLD, PORT_WORLD)

    def A_to_pack(self, product_id, description, quantity, ship_id):
        command = world_amazon_pb2.ACommands()
        command.simspeed = SIMSPEED
        # filling info of topack
        # type: Apack
        pack = command.topack.add()

        pack.whnum = 0
        pack.shipid = ship_id
        pid = pack.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command, self.sock)

    def APurchase(self, product_id, description, quantity):
        command = world_amazon_pb2.ACommands()
        command.simspeed = 50000
        purchase = command.buy.add()
        purchase.whnum = 0
        pid = purchase.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command, self.sock)
