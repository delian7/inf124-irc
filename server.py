from network import Listener, Handler, poll
from collections import deque

SERVER_PORT = 8888
HOST = ""
handlers = {}  # map client handler to user name

def createMenu():
	opening = "Please choose from the following menu (Enter the number):"
	option1 = "1: Change order"
	option2 = "2: Cancel order"
	option3 = "3: Get ETA"
	option4 = "4: Ask general questions?"
	option5 = "5: Exit"

	return opening + "\n" + option1 + "\n" + option2 + "\n" + option3 + "\n" + option4 + "\n" + option5

client_msgs = deque([])
client_handlers = deque([])
agentAddress = None
agent_free = False
agent_handler = None

class MyHandler(Handler):

	def on_open(self):
		pass

	def on_close(self):
		self.close()

	def on_msg(self, msg):
		if type(msg) is dict:
			if 'type' in msg and msg['type'] == "agent":
				if 'join' in msg:
					print msg
					global agentAddress
					agentAddress = msg['address']
					global agent_handler
					agent_handler = self
					self.set_free()
					agent_handler.do_send("Hello Agent " + msg['join'] + "\n" + "Lets wait for a customer....\n")
				elif 'quit' in msg:
					print "User Quit. Waiting for another user...."
					self.set_free()
					print "Free"
					self._check_waiting()
				#todo
			else:
				if 'join' in msg:
					print msg
					self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
				elif 'option' in msg:
					global client_handlers
					client_handlers.append(self)
					print msg
					agentMessage = "Checking for available agent now..."
					self.do_send('You would like to ' + msg['option'] + '. ' + agentMessage  + "\n")
					self._check_agent(msg)

		else: 
			print msg
	

	def _notify_agent(self, option, name):
		agent_handler.do_send("The person we are about to connect you to wants to talk about:\n" + option + "\n")
		agent_handler.do_send("You're now chatting with:\n" + name + "\n")

	def _check_agent(self, msg):
		if agent_free:
			self._take_client()
			self._notify_agent(msg["option"], msg['name'])
			self._init_chat()
		else:
			self.do_send("Agent is busy. You will now be added into a queue.\nPlease wait....\n")
			global client_msgs
			client_msgs.append(msg)

	def _take_client(self):
		global agent_free
		agent_free = False
		self.do_send("Now connecting to an agent.\n")

	def _init_chat(self):
		global client_handlers
		handler = client_handlers.popleft()
		handler.do_send({'type': "agent-connect", "address":agentAddress})

	def set_free(self):
		global agent_free
		agent_free = True

	def _check_waiting(self):
		if len(client_handlers) > 0:
			global client_msgs
			self._check_agent(client_msgs.popleft())
	

# server = ServerListener(port, MyHandler)

server = Listener(SERVER_PORT, MyHandler)

while 1:
	poll(timeout=0.05) # in seconds
