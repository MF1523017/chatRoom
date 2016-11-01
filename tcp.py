# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:38:02 2016
@author: lipei 


""" 

from socket import *
import select#select 模块提供了异步I/O
import sys
class Tcp:
    def __init__(self,HOST,PORT,BUFSIZE):
        self._host=HOST#hostname ,ip address in general
        self._port=PORT#port of the computer
        self._bufferSize=BUFSIZE
        self._address=(HOST,PORT)
    def build(self):
        self._INIT()#这里我们定义了build接口，并没有定义INIT方法，由下面的子类来实现，
class TcpServer(Tcp):
    def __init__(self,HOST,PORT,BUFSIZE,CONNECTIONS=None):
        Tcp.__init__(self,HOST,PORT,BUFSIZE)
        self.__tcpSerSock=socket(AF_INET,SOCK_STREAM)#we create the server socket
        if CONNECTIONS is None:#variable 
            CONNECTIONS=[]
            self.CONNECTIONS=CONNECTIONS		
    def _INIT(self):
        self.__tcpSerSock.bind(self._address)#bind
        self.__tcpSerSock.listen(5)#listen
        self.CONNECTIONS.append(self.__tcpSerSock)
        print 'Chat Server stared on port {}'.format(self._port)
    def communication(self):
        print 'waiting for connection...'
        while True:
		#select I/O 
            readSock,writeSock,errorSock=select.select(self.CONNECTIONS,[],[])
            for sock in readSock:
                if sock==self.__tcpSerSock:#accept the client connecting
                    tcpCliSock,addr=self.__tcpSerSock.accept()
                    print '...connected from:',addr
                    self.CONNECTIONS.append(tcpCliSock)
		#tell other clients
                    self.__broadcastData(tcpCliSock,'[{}]entered room'.format(addr))
                else:
                    try:
                        #recieve the data from the client
                        data=sock.recv(self._bufferSize)
                        if data:
                            #tell other clients
                            self.__broadcastData(sock,'r[{}]'.format(addr)+' '+data)
                    except:
                        self.__broadcastData(sock,'Client {} is offline '.format(addr))
                        print 'Client {} is offline '.format(addr)
                        sock.close()
                        self.CONNECTIONS.remove(sock)
                        continue
		
    def __del__(self):
        self.__tcpSerSock.close()
    def __broadcastData(self,sock,message):
        for socket in self.CONNECTIONS:
            if socket!=self.__tcpSerSock and socket!=sock:#except for server and itself
                try:
                    socket.send(message)
                except:
                    socket.close()
                    self.CONNECTIONS.remove(socket)
class TcpClient(Tcp):
    def __init__(self,HOST,PORT,BUFSIZE):
        Tcp.__init__(self,HOST,PORT,BUFSIZE)
        self.__tcpCliSock=socket(AF_INET,SOCK_STREAM)
    def _INIT(self):
        self.__tcpCliSock.connect(self._address)
        self.__tcpCliSock.settimeout(2)
    def communication(self):
        while True:
	#only input and the other client message
            socketList=[sys.stdin,self.__tcpCliSock]
            readSock,writeSock,errorSock=select.select(socketList,[],[])
            for sock in readSock:
                #recieve the data from the server
                if sock==self.__tcpCliSock:
                    data=sock.recv(self._bufferSize)
                    if not data:
                        print '\nDisconnected from chat server'
                        sys.exit()
                    else:
                        sys.stdout.write(data)
                        self.__prompt()
                else:
		#input
                    msg=sys.stdin.readline()
                    if msg in ['q\n','quit\n','QUIT\n','Q\n']:
                        sys.exit()
                    self.__tcpCliSock.send(msg)
                    self.__prompt()
    def __del__(self):
        self.__tcpCliSock.close()
    def __prompt(self):
        sys.stdout.write('<You>')
        sys.stdout.flush() 
