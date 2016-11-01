# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:11:06 2016

@author: lipei
"""

from socket import *
import select#select 模块提供了异步I/O
from tcp import Tcp
import sys
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


if __name__=='__main__':
    if len(sys.argv)!=2:
        print 'Usage:python client.py hostname'
        sys.exit()
    host=sys.argv[1]
    #port=int(sys.argv[2])
    port=23456
    tc=TcpClient(host,port,1024)#change the ipaddr if you use the code
    tc.build()
    tc.communication()
