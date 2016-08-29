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
def fib(x):
    sleep(0.005)
    if x<2:
        return 1
    return (fib(x-1)+fib(x-2))

def fac(x):
    sleep(0.1)
    if x<2:
        return 1
    return (x*fac(x-1))

def Sum(x):
    sleep(0.1)
    if x<2:
        return 1
    return (x+Sum(x-1))

funcs=[fib,fac,Sum]
n=15

class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name=name
        self.func=func
        self.args=args
    def __call__(self):#特殊的函数
        apply(self.func,self.args)
#    def loop(nloop,nsec):
#        print 'start loop',nloop,'at:',ctime()
#        sleep(nsec)
#        print 'loop',nloop,'done at:',ctime()

#从Thread派生出一个子类，创建一个这个子类的实例
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        print 'starting',self.name,'at',ctime()
        self.res=apply(self.func,self.args)
        print self.name,'finished at:',ctime()
    def getResult(self):
        return self.res
if __name__=='__main__':
    print 'starting at:',ctime()
    threads=[]
    nfuncs=range(len(funcs))
    print '***single thread'
    for i in nfuncs:
        print 'starting',funcs[i].__name__,'at:',ctime()
        print funcs[i](n)
        print funcs[i].__name__,'finished at:',ctime()
    print '**multiple threads'
    for i in nfuncs:
        t=MyThread(funcs[i],(n,),funcs[i].__name__)
        threads.append(t)
    print threading.activeCount()
    for i in nfuncs:
        threads[i].start()
    
    for i in nfuncs:
        threads[i].join()#对每个线程调用join()所有的线程就会创建以后，再一起调用start()函数，而不是创建一个启动一个。这样不用
        print threads[i].getResult()               #再管理一堆锁（分配锁，获得锁，释放锁，检查锁等状态）
                        #
    print 'all Done at:',ctime()
    