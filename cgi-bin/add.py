# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 22:08:41 2016

@author: lipei
"""

import sys
def add(args):
    return sum(map(int,args.split()))
if __name__=='__main__':
    if len(sys.argv)!=2:
        print 'Usage:python add.py args'
        sys.exit()
    print add(sys.argv[1])