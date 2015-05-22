from network import Listener, Handler, poll



handlers = {}  # map client handler to user name

class MyHandler(Handler):

	def on_open(self):
		pass

	def on_close(self):
		pass

	def on_msg(self, msg):
		print msg
		self.do_send(msg)


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
while 1:
	poll(timeout=0.05) # in seconds
