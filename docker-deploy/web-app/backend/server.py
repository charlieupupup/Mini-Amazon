import base
import IG1_pb2
import world_amazon_pb2

# allow connection from all host
HOST = ''
# GROUP 1 port
PORT = 33333


class Server(Base):
    """
    info from ups
    """

    def ups(self, trans):
        while (True):
            str = self.recv(self.Usock)
            if (len(str) > 0):
                response = IG1_pb2.IG1()
                response.ParseFromString(str)
                print(response)
                if (response != None):
                    self.ALoad(trans.ship_id, response.truckid)
                    trans.package_id = response.packageid
                    trans.save()
                    return

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
