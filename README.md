#chatRoom
tcp.py: class Tcp
	class TcpServer(Tcp)
	class TcpClient(Tcp)
server.py:
	you can change the port and the buffersize
	usage :python server.py
client.py:
	usage:python client.py hostname(ip address) port

usage:
	1 open a terminal 
	2 python server.py 
	3 open other new terminals (you can choose other computers)
	4 python client.py
	5 talk
depend:
	python 2.7
