from network import Handler, poll
import sys
from threading import Thread
from time import sleep

<<<<<<< HEAD
agent_free = True
=======
>>>>>>> 626b3d66b7f2377b9fe7000a9d03b6d55294a03b

myname = raw_input('What is your name? ')

class Client(Handler):

    def on_close(self):
        pass

    def on_msg(self, msg):
        print msg

host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
<<<<<<< HEAD
                            
=======


def change_order():
    order_number = raw_input("What is your order number?")




>>>>>>> 626b3d66b7f2377b9fe7000a9d03b6d55294a03b
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()

while 1:
    mytxt = sys.stdin.readline().rstrip()
    options = {'1':'change order', '2':'cancel order', '3':'get ETA', '4':'ask general questions'}
    if mytxt in options:
        client.do_send({'option': options[mytxt], 'txt': mytxt})
    elif mytxt == '5':
        print "Closing connection to server."
        sys.exit()
    else:
        print "Please enter a number from 1-5."
