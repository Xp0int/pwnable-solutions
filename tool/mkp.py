#!/bin/python2.7
# -*- coding:utf-8 -*-

from zio import *

# print
GREEN   = COLORED(RAW, 'green')
CYAN    = COLORED(RAW, 'cyan')

# extension for zio
# write
def w(self, s): 
    self.write(s)

# writeline
def wl(self, s = ''): 
    if isinstance(s, (int, long)):
        self.writeline(str(s)) 
    else: 
        self.writeline(s)

# writelines
def ws(self ,sequence): 
    self.writelines( [str(i) if isinstance(i, (int, long)) else i for i in sequence] )

# read
def r(self, size = None, timeout = 1):
    return self.read(size, timeout)

# readline
def rl(self, size = 1):
    return self.read_line(size)

# read_until
def ru(self, pattern_list, timeout = 1, searchwindowsize = None):
    return self.read_until(pattern_list, timeout, searchwindowsize)

def wa(self, pattern_list, s, timeout = -1, searchwindowsize = None):
    self.read_until(pattern_list, timeout, searchwindowsize)
    self.writeline(s)

# writeline_after
def wla(self, pattern_list, s, timeout = 1, searchwindowsize = None):
    self.read_until(pattern_list, timeout, searchwindowsize) 
    self.writeline(s)

# wrtelins_after
def wsa(self, pattern_list, sequence, timeout = 1, searchwindowsize = None):
    self.read_until(pattern_list, timeout, searchwindowsize) 
    self.writelines( [str(i) if isinstance(i, (int, long)) else i for i in sequence] )

# main
setattr(zio, 'w', w)
setattr(zio, 'wl', wl)
setattr(zio, 'ws', ws)
setattr(zio, 'wa', wa)
setattr(zio, 'wla', wa)
setattr(zio, 'wsa', wsa)
setattr(zio, 'r', r)
setattr(zio, 'rl', rl)
setattr(zio, 'ru', ru)

# utilities
def info_leak(arg1, arg2):
    print GREEN("[_] {} => {}".format(arg1, arg2))

def info_found(arg1, arg2):
    print CYAN("[+] {} :  {}".format(arg1, arg2))

def mkp(target, debug = True):
    if debug:
        return zio(target, print_read = COLORED(REPR, 'red'), print_write = COLORED(REPR, 'yellow'), timeout = 10000)
    else:
        return zio(target, print_read = False, print_write = False, timeout = 10000)

__all__ = ['info_leak', 'info_found', 'mkp']
