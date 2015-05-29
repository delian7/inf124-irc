from network import Listener, Handler, poll, get_my_ip
import sys
from threading import Thread
from time import sleep
from random import randint

client = None
handler = None

class Agent(Handler):
	def __init__ (self, host, port, sock=None):
		Handler.__init__(self, host, port, sock)

	def on_msg(self, msg):
		#todo
		if type(msg) is dict:
		    ip, port = msg['address'].split(":")
		    print msg['address']
		    global client
		    client = Listener(AGENT_PORT, ClientConnect)
		else:
			print msg

	def on_close(self):
		pass

class ClientConnect(Handler):

    def on_close(self):
        pass

    def on_msg(self, msg):
        print msg

    def on_open(self):
    	global handler
    	handler = self
    	print "Now Connected"


name = raw_input("\n\n" + "*" * 40 + "\n"
	+ "*     Welcome to MobaBoba Chat!        *\n" +
	"*" * 40 + "\n\n"
	"Please enter your name, agent: ")
host, port = '128.195.6.146', 8888
AGENT_PORT = randint(20000,30000)
address = get_my_ip() + ":" + str(AGENT_PORT)
agent = Agent(host, port)
agent.do_send({'type':"agent", "address":address, "join":name})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()

while 1:
	mytxt = raw_input()
	handler.do_send(mytxt)
    #todo
    # mytxt = sys.stdin.readline().rstrip()
    # client.do_send({'type':"chat", "msg":mytxt})