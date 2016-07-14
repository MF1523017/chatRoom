# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:43:13 2016
learning thread
@author: lipei
"""

import threading
from time import sleep,ctime

loops=[4,2]
#创建一个Thread的实例，传给它一个函数

def loop(nloop,nsec):
    print 'start loop',nloop,'at:',ctime()
    sleep(nsec)
    print 'loop',nloop,'done at:',ctime()
#创建一个Thread 的实例，传给它一个类


class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name=name
        self.func=func
        self.args=args
    def __call__(self):
        apply(self.func,self.args)
#    def loop(nloop,nsec):
#        print 'start loop',nloop,'at:',ctime()
#        sleep(nsec)
#        print 'loop',nloop,'done at:',ctime()
if __name__=='__main__':
    print 'starting at:',ctime()
    threads=[]
    nloops=range(len(loops))
    for i in nloops:
        t=threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__))
        threads.append(t)
    
    for i in nloops:
        threads[i].start()
    
    for i in nloops:
        threads[i].join()#对每个线程调用join()所有的线程就会创建以后，再一起调用start()函数，而不是创建一个启动一个。这样不用
                        #再管理一堆锁（分配锁，获得锁，释放锁，检查锁等状态）
                        #
    print 'all Done at:',ctime()
    