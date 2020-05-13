from .ups import UPS
from .world import World

import threading
HOST_UPS = 'vcm-12423.vm.duke.edu'
PORT_UPS = 33333

HOST_WORLD = 'vcm-12423.vm.duke.edu'
PORT_WORLD = 23456

SIMSPEED = 10000


class Back():
    def __init__(self):
        self.ups = UPS(HOST_UPS, PORT_UPS, SIMSPEED)
        print('ups initialized')
        self.world = World(HOST_WORLD, PORT_WORLD, SIMSPEED)
        print('world initialized')
        self.ups.setWorld(self.world)
        self.world.setUPS(self.ups)
        print('set completed')
        self.ups.init()
        print('backend inited')

    def buy(self, pid, whid, count):
        self.world.purchase_more(pid, whid, count)

    def pack(self, pkgid):
        self.world.pack(pkgid)

    def refresh(self):
        self.world.query()

