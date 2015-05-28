from network import Listener, Handler, poll

AGENT_PORT = 9999
SERVER_PORT = 8888
handlers = []  # map client handler to user name
agent_free = True;

class Agent(Handler):
	def __init__(self, host, port):
		Handler.__init__(host, port)

	def on_msg(self, msg):
		self.do_send(msg)

	def on_open(self):
		pass

	def on_close(self):
		pass

def createMenu():
	opening = "Please choose from the following menu (Enter the number):"
	option1 = "1: Change order"
	option2 = "2: Cancel order"
	option3 = "3: Get ETA"
	option4 = "4: Ask general questions?"
	option5 = "5: Exit"

	return opening + "\n" + option1 + "\n" + option2 + "\n" + option3 + "\n" + option4 + "\n" + option5


def output_to_file():
        pass
# =======
# def init_chat():
# 	if type(msg) is dict:
# 		if 'join' in msg:
# 			print msg
# 			self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
# 		elif 'option' in msg:
# 			print msg
# 			agentMessage = "Checking for available agent now..."
# 			self.do_send('You would like to ' + msg['option'] + '. ' + agentMessage +"\n")
# 			agent.connect(("", AGENT_PORT))
# 			return 
# >>>>>>> Stashed changes


class MyHandler(Handler):

	def on_open(self):
                pass

	def on_close(self):
		pass

	def on_msg(self, msg):
		if type(msg) is dict:
			if 'join' in msg:
				print msg
				self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
			elif 'option' in msg:
				print msg
				agentMessage = "Checking for available agent now..."
				self.do_send('You would like to ' + msg['option'] + '. ' + agentMessage)
		else:
			print msg

# =======
# 		if agent_free:
# 			self.connect(("", AGENT_PORT))
# 			init_chat()
# 		else:
# 			handlers.append(self)

					
			
class ServerListener(Listener):

	#inherits from listener
	def __init__(self, port, handler_class):
		Listener.__init__(self, port, handler_class)
		self.connections = []
		

	def handle_accept(self):
		Listener.handle_accept(self)
		self.print_clients()

	def print_clients(self):
		for item in self.connections:
			print str(item[0]) + " " + str(item[1])




port = 8888
server = ServerListener(port, MyHandler)

# server = ServerListener(SERVER_PORT, MyHandler)
# agent = Agent("localhost", AGENT_PORT)

while 1:
	poll(timeout=0.05) # in seconds
