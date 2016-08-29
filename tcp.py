# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:38:02 2016
@author: lipei 


""" 

from socket import *
import select#select 模块提供了异步I/O
import threading
import sys
class Tcp:
    def __init__(self,HOST,PORT,BUFSIZE):
        self.host=HOST
        self.port=PORT
        self.bufferSize=BUFSIZE
        self.address=(HOST,PORT)
    def build(self):
        self.INIT()#这里我们定义了build接口，并没有定义INIT方法，由下面的子类来实现，
    @staticmethod
    def Recv(tcpCliSock,buffers):
        data=tcpCliSock.recv(buffers)
        print data
    @staticmethod
    def Send(tcpCliSock):
        sendData=raw_input('> ')
        if sendData in ['q','Q','quit','QUIT']:
            os.abort()
        tcpCliSock.send(sendData)

    def buildThread(self):
        #创建两个线程，来分别实现发送和接收数据
        reciveT=threading.Thread(target=Tcp.Recv,args=(self.tcpCliSock,self.bufferSize))#这里的self.tcpCliSock我们也没有定义，由下面的子类来提供，这是oop常用的架构，
        sendT=threading.Thread(target=Tcp.Send,args=(self.tcpCliSock,))#由子类来实现超类提供的接口
        for t in (reciveT,sendT):
            t.start()
        for t in (reciveT,sendT):
            t.join()
class TcpServer(Tcp):
    def __init__(self,HOST,PORT,BUFSIZE,CONNECTIONS=None):
        Tcp.__init__(self,HOST,PORT,BUFSIZE)
        self.tcpSerSock=socket(AF_INET,SOCK_STREAM)
	if CONNECTIONS is None:
	    CONNECTIONS=[]
	self.CONNECTIONS=CONNECTIONS		
    def INIT(self):
        self.tcpSerSock.bind(self.address)
        self.tcpSerSock.listen(5)
	self.CONNECTIONS.append(self.tcpSerSock)
	print 'Chat Server stared on port {}'.format(self.port)
    def communication(self):
        print 'waiting for connection...'
        while True:
	    readSock,writeSock,errorSock=select.select(self.CONNECTIONS,[],[])
	    for sock in readSock:
		if sock==self.tcpSerSock:
            	    tcpCliSock,addr=self.tcpSerSock.accept()
            	    print '...connected from:',addr
	    	    self.CONNECTIONS.append(tcpCliSock)
		    self.broadcastData(tcpCliSock,'[{}]entered room'.format(addr))
		else:
		    try:
			data=sock.recv(self.bufferSize)
			if data:
			    self.broadcastData(sock,'r'+' '+data)
		    except:
			self.broacastData(sock,'Client {} is offline '.format(addr))
			print 'Client {} is offline '.format(addr)
			sock.close()
			self.CONNECTIONS.remove(sock)
			continue
		
    def __del__(self):
        self.tcpSerSock.close()
    def broadcastData(self,sock,message):
	for socket in self.CONNECTIONS:
	    if socket!=self.tcpSerSock and socket!=sock:
		try:
		    socket.send(message)
		except:
		    socket.close()
		    self.CONNECTIONS.remove(socket)
class TcpClient(Tcp):
    def __init__(self,HOST,PORT,BUFSIZE):
        Tcp.__init__(self,HOST,PORT,BUFSIZE)
        self.tcpCliSock=socket(AF_INET,SOCK_STREAM)
    def INIT(self):
        self.tcpCliSock.connect(self.address)
    def communication(self):
        while True:
	    socketList=[sys.stdin,self.tcpCliSock]
	    readSock,writeSock,errorSock=select.select(socketList,[],[])
	    for sock in readSock:
		if sock==self.tcpCliSock:
		    data=sock.recv(self.bufferSize)
		    if not data:
			print '\nDisconnected from chat server'
			sys.exit()
		    else:
			sys.stdout.write(data)
			self.prompt()
		else:
		    msg=sys.stdin.readline()
		    self.tcpCliSock.send(msg)
		    self.prompt()
    def __del__(self):
        self.tcpCliSock.close()
    def prompt(self):
	sys.stdout.write('<You>')
	sys.stdout.flush() 
