import base
import IG1_pb2

# allow connection from all host
HOST = ''
# GROUP 1 port
PORT = 33333


class Server(Base):
    def process_Uresponse(self, trans):
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
