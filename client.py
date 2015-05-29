from network import Handler, poll, get_my_ip
import sys
from threading import Thread
from time import sleep
from random import randint
# from server import output_to_file

agent = None

myname = raw_input('What is your name? ')

class Client(Handler):

    def on_close(self):
        pass

    def on_msg(self, msg):
        if type(msg) is dict:
            ip, port = msg['address'].split(":")
            global agent
            agent = AgentConnect(ip, int(port))
        else:
            print msg       


class AgentConnect(Handler):
    def on_close(self):
        pass

    def on_msg(self, msg):
        self.do_send({"type":"chat", "msg":msg})

    def on_open(self):
        print "Now Connected"

    



host, port = 'localhost', 8888
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
    mytxt = sys.stdin.readline().rstrip()
    options = {'1':'change order', '2':'cancel order', '3':'get ETA', '4':'ask general questions'}
    if agent:
        agent.do_send({'type':"agent", "msg": mytxt})
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
            client.do_send({'option': options[mytxt], 'txt': mytxt})
        elif mytxt == '5':
            print "Closing connection to server."
            sys.exit()
        else:
            print "Please enter a number from 1-5."
