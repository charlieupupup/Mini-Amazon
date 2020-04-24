from .ups import UPS
from .world import World

import threading
HOST_UPS = 'vcm-14579.vm.duke.edu'
PORT_UPS = 33333

HOST_WORLD = 'vcm-14579.vm.duke.edu'
PORT_WORLD = 23456

SIMSPEED = 100


class Back:
    def __init__(self):
        self.ups = UPS(HOST_UPS, PORT_UPS, SIMSPEED)
        print('ups initialized')
        self.world = World(HOST_WORLD, PORT_WORLD, SIMSPEED)
        print('world initialized')
        self.ups.setWorld(self.world)
        self.world.setUPS(self.ups)
        print('ups init')

        # init
        th_init = threading.Thread(target=self.ups.init, args=())
        th_init.setDaemon(True)
        th_init.start()

        # self.world.init(0)

    def buy(self, pid, whid, count):
        self.world.purchase_more(pid, whid, count)

    def pack(self, pkgid):
        self.world.pack(pkgid)

    def refresh(self):
        self.world.query()

# # email set up
# smtp_server = "smtp.gmail.com"
# email_port = 587  # For starttls
# sender_email = "568.hw1.yh218.yx139@gmail.com"
# password = 'QWE123!@#'
#
# # send email to user
#
#
# def SendEmail(db, packageid):
#     global smtp_server
#     global email_port
#     global sender_email
#     global password
#     message = 'Your package ' + str(packageid) + ' has been delivered!'
#     message = 'Subject: Package Delivered\n\n' + message
#     context = ssl.create_default_context()
#     receiver_email = GetEmail(db, packageid)
#     if receiver_email == -1:
#         return
#     with smtplib.SMTP(smtp_server, email_port) as server:
#         server.ehlo()  # Can be omitted
#         server.starttls(context=context)
#         server.ehlo()  # Can be omitted
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
