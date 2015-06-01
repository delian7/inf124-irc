"""
PLEASE READ THE READ ME FIRST!!!!!!!!!!
"""

from network import Listener, Handler, poll
from collections import deque
import sys

SERVER_PORT = 8888
HOST = ""

def createMenu():
	#used to update client view
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
current_handler = None

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
					agent_handler.do_send("\nHello Agent " + msg['join'] + "\n" + "Lets wait for a customer....\n")
				elif 'quit' in msg:
					agent_handler.do_send("User Quit. Waiting for another user....\n")
					self.set_free()

					#checks to see if others are waiting
					self._check_waiting()
				#todo
			else:
				if 'join' in msg:
					print msg
					self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
				elif 'option' in msg:

					#add to clients handlers for when we need to notify them..
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
			#take the chat
			self._take_client()
			self._notify_agent(msg["option"], msg['name'])
			self._init_chat()
		else:
			self.do_send("Agent is busy. You will now be added into a queue.\nPlease wait....\n")
			#add the name and the option to a msg list for later connections
			global client_msgs
			client_msgs.append(msg)

	def _take_client(self):
		#makes agent budy
		global agent_free
		agent_free = False

	def _init_chat(self):
		#gets rid of the handler to the client being taken
		global client_handlers
		handler = client_handlers.popleft()
		global current_handler
		current_handler = handler
		handler.do_send("Now connecting to an agent.\n")
		handler.do_send({'type': "agent-connect", "address":agentAddress})

	def set_free(self):
		#sets agent free
		global agent_free
		agent_free = True

	def _check_waiting(self):
		#checks to see if there are any clients waiting
		if len(client_handlers) > 0:
			global client_msgs
			self._check_agent(client_msgs.popleft())
	

server = Listener(SERVER_PORT, MyHandler)

while 1:
	try:
		poll(timeout=0.05) # in seconds
	except:
		if agent_handler:
			agent_handler.do_send("Server Disconnected... Now Closing")
			agent_handler.do_send({"kill":""})
			agent_handler.close()
		if current_handler:
			current_handler.do_send("Server Disconnected... Now Closing")
			current_handler.do_send({"kill":""})
			current_handler.close()
		for handler in client_handlers:
			handler.do_send("Server Disconnected... Now Closing")
			handler.do_send({"kill":""})
			handler.close()
		print "SERVER QUIT"
		server.close()
		sys.exit()


