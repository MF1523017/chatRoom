# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:11:06 2016

@author: lipei
"""


from tcp import TcpClient
import sys

if __name__=='__main__':
    if len(sys.argv)<3:
	print 'Usage:python client.py hostname port'
	sys.exit()
    host=sys.argv[1]
    port=int(sys.argv[2])
    tc=TcpClient(host,port,1024)#change the ipaddr if you use the code
    tc.build()
    tc.communication()
