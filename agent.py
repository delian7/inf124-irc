"""
PLEASE READ THE READ ME FIRST!!!!!!!!!!
"""


from network import Listener, Handler, poll, get_my_ip
import sys
from threading import Thread
from time import sleep
from random import randint

name = raw_input("\n\n" + "*" * 40 + "\n"
	+ "*     Welcome to MobaBoba Chat!        *\n" +
	"*" * 40 + "\n\n"
	"Please enter your name, agent: ")
host, port = '128.195.6.162', 8888
AGENT_PORT = randint(20000,30000)
ag_string = "Agent (" + name +  "): "
cl_string = "Client: "
quit = False

# print get_my_ip() + " Listener PORT:" + str(AGENT_PORT)
address = get_my_ip() + ":" + str(AGENT_PORT)

handler = None
server_handler = None

def kill():
	global quit
	quit = True


def output_to_file(log):
	result = ''
	with open('chatlog.txt', 'a') as f:
		for line in log:
			f.write(line+"\n")
			result += line + "\n"
	return result


class Agent(Handler):
	def __init__ (self, host, port, sock=None):
		Handler.__init__(self, host, port, sock)

	def on_msg(self, msg):
		#todo
		if type(msg) is dict:
			if "address" in msg:
			    ip, port = msg['address'].split(":")
			    print msg['address']
			elif "kill" in msg:
				print "Press Enter to end session"
				handler.close()
				client.close()
				kill()
		else:
			print msg

	def on_close(self):
		pass

	def on_open(self):
		global server_handler
		server_handler = self

class ClientConnect(Handler):
	
	def __init__(self, host, port, sock=None):
		Handler.__init__(self, host, port, sock)
		self.log = []

	def on_close(self):
		pass

	def on_msg(self, msg):
		if msg == ":q":
			#destroy the chat
			self.log = []
			server_handler.do_send({'quit':":q", 'type':'agent'})
		elif msg == ":s":
			chat = output_to_file(self.log)
			handler.do_send({'chat':chat})
		else:
			self.log.append(cl_string + msg)
		print cl_string + msg

	def on_open(self):
		global handler
		handler = self
		print "Now Connected"
		
	def appendChat(self, msg):
		self.log.append(msg)



#create a listener for all single chats
client = Listener(AGENT_PORT, ClientConnect)

#create a connection to the server
agent = Agent(host, port)
agent.do_send({'type':"agent", "address":address, "join":name})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()

while not quit:
	mytxt = raw_input("")
	handler.do_send(ag_string + mytxt)
	handler.appendChat(ag_string + mytxt)