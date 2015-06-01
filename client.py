from network import Listener, Handler, poll, get_my_ip
import sys
from threading import Thread
from time import sleep
from random import randint
# from server import output_to_file

agent = None


class Client(Handler):

    def on_close(self):
        pass

    def on_msg(self, msg):
        if type(msg) is dict:
            ip, port = msg['address'].split(":")
            print msg['address']
            global agent
            agent = AgentConnect(ip , int(port))
        else:
            print msg       

class AgentConnect(Handler):
    def on_close(self):
        pass

    def on_msg(self, msg):
        print msg

    def on_open(self):
        print "Now Connected"


myname = raw_input("\n\n" + "*" * 40 + "\n"
    + "*       Welcome to MobaBoba Chat!      *\n" +
    "*" * 40 + "\n\n"
    "Please enter your name: ")
host, port = '128.195.6.162', 8888
CLIENT_PORT = randint(20000,30000)
address = get_my_ip() + ":"  + str(CLIENT_PORT)
client = Client(host, port)
client.do_send({'join': myname, "address":address})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()

while 1:
    mytxt = raw_input("")
    options = {'1':'change order', '2':'cancel order', '3':'get ETA', '4':'ask general questions'}
    if agent:
        agent.do_send(mytxt)
        if mytxt == ':e':
            print 'lolololololol'
        elif mytxt == ":s":
            #todo
            pass
        elif mytxt == ":q":
            print "Closing connection to server."
            sys.exit()
    else:
        if mytxt in options:
            client.do_send({'option': options[mytxt], 'txt': mytxt, "name":myname})
        elif mytxt == '5':
            print "Closing connection to server."
            sys.exit()
        else:
            print "Please enter a number from 1-5."
