from network import Listener, Handler, poll
from collections import deque

SERVER_PORT = 8888
HOST = "localhost"
handlers = {}  # map client handler to user name

def createMenu():
	opening = "Please choose from the following menu (Enter the number):"
	option1 = "1: Change order"
	option2 = "2: Cancel order"
	option3 = "3: Get ETA"
	option4 = "4: Ask general questions?"
	option5 = "5: Exit"

	return opening + "\n" + option1 + "\n" + option2 + "\n" + option3 + "\n" + option4 + "\n" + option5

clients = deque([])
agentAddress = None
agent_free = True
agent_handler = None

class MyHandler(Handler):

	def __init__ (self, host, port, sock=None):
		Handler.__init__(self, host, port, sock)

	def on_open(self):
		pass

	def on_close(self):
		pass

	def on_msg(self, msg):
		if type(msg) is dict:
			if 'type' in msg and msg['type'] == "agent":
				agent_handler = self
				agentAddress = msg['address']
				agent_free = True
				agent_handler.do_send("HI!")
				#todo
			else:
				if 'join' in msg:
					clients.append(msg['address'])
					print msg
					self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
				elif 'option' in msg:
					print msg
					agentMessage = "Checking for available agent now..."
					self.do_send('You would like to ' + msg['option'] + '. ' + agentMessage  + "\n")
					self._check_agent()
					self._init_chat()

		else:
			print msg
	

	def _check_agent(self):
		if agent_free:
			self._take_client()
			return
		else:
			self.do_send("Agent is busy. You will now be added into a queue.\nPlease wait....\n")
			while not agent_free:
				pass
			self._take_client()
			return

	def _take_client(self):
		agent_free = False
		agent_handler.do_send({"address":clients.popleft()})
		self.do_send("Now connecting to an agent.\n")

	def _init_chat(self):
		self.do_send({'type': "agent-connect", "address":agentAddress})



# port = 8888
# server = ServerListener(port, MyHandler)

server = Listener(SERVER_PORT, MyHandler)

while 1:
	poll(timeout=0.05) # in seconds
