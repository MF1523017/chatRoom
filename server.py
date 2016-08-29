# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:07:47 2016

@author: lipei
"""

from tcp import TcpServer,TcpClient

if __name__=='__main__':
    ts=TcpServer('',23456,1024)
    ts.build()
    ts.communication()
    