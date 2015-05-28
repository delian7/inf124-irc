from network import Listener, Handler, poll

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

	return opening + "\n" + option1 + "\n" + option2 + "\n" + option3 + "\n" + option4 + "\n" + option


class MyHandler(Handler):
	

	def on_open(self):
                pass

	def on_close(self):
		pass

	def on_msg(self, msg):
		if type(msg) is dict:
			if 'type' in msg and msg['type'] == agent:
				#todo
			else:
				if 'join' in msg:
					print msg
					self.do_send('Hello ' + msg['join'] + '!\n' + createMenu())
				elif 'option' in msg:
					print msg
					agentMessage = "Checking for available agent now..."
					self.do_send('You would like to ' + msg['option'] + '. ' + agentMessage)
					self.do_send(check_agent())

		else:
			print msg
	

	def _check_agent():
		if agent_free:
			return "Now connecting to an agent.", 
		else:
			return "Agent is busy. You will now be added into a queue.\n Please wait...."

	def _init_chat(self):
		if agent_free:

					
			
class ServerListener(Listener):
	#inherits from listener

	def __init__(self, port, handler_class):
		Listener.__init__(self, SERVER_PORT, handler_class)
		self.clients = []
		self.agents = []
		self.agent_free = True;
		

	def handle_accept(self):
		accept_result = self.accept()
        if accept_result:  # None if connection blocked or aborted
            sock, (host, port) = accept_result
            h = self.handler_class(host, port, sock)
            self.on_accept(h)
            h.on_open()
            self.connections.append((port, host, sock))

	def print_clients(self):
		for item in self.connections:
			print str(item[0]) + " " + str(item[1])



# port = 8888
# server = ServerListener(port, MyHandler)

server = ServerListener(SERVER_PORT, MyHandler)

while 1:
	poll(timeout=0.05) # in seconds
