from network import Handler, poll

class Agent(Handler):
	def __init__(self, host, port):
		Handler.__init__(host, AGENT_PORT)

	def on_msg(self, msg):
		#todo

	def on_open(self):
		pass

	def on_close(self):
		pass




host, port = 'localhost', 8888
agent = Agent(host, port)
agent.do_send({'type': 'agent'})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()

while 1:
    #todo
