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

