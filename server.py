from network import Listener, Handler, poll

handlers = {}  # map client handler to user name

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
		else
            print msg

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
