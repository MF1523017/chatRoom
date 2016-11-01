# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:07:47 2016

@author: lipei
"""

from tcp import Tcp
from socket import *
import select#select 模块提供了异步I/O
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

if __name__=='__main__':
    ts=TcpServer('',23456,1024)
    ts.build()
    ts.communication()
    