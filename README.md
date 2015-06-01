BEFORE YOU RUN, YOU MUST BE ON THE SAME LOCAL NETWORK
OTHERWISE ERRORS WILL ENSUE!!!

IF YOU GET ERRORS DUE TO "get_my_ip()" IN THE network.py, 
IT IS NOT IN OUR CONTROL. THIS HAS SOMETHING TO DO WITH YOUR
MACHINE. MOST LIKELY A COMPATIBILITY ISSUE. USE LATEST PYTHON 2.7.X



You must run in this sequence to ensure completeness:

server -> agent -> client

Agents must log in before any clients connect!!!!

":s" saves on both the client and agent sides.

"ctrl + C" to kill the server. This will then kill the clients and agents.

If you're running your own server instance... please make sure
to either:

	-run localhost
	-change the hardcoded IP address in both agent and client