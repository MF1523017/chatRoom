# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:11:06 2016

@author: lipei
"""


from tcp import TcpClient

if __name__=='__main__':
    tc=TcpClient('localhost',23456,1024)#change the ipaddr if you use the code
    tc.build()
    tc.communication()
