#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

'''
By Icemakr

This is a useless script for my daily pwning in CTFs:(

Note that I use zio instead of pwntool because of its lightweight.
'''

# zio is awesome
from zio import *

# print
BLUE    = COLORED(RAW, color = 'blue', attrs = ['bold'])
GREEN   = COLORED(RAW, color = 'green', attrs = ['bold'])
CYAN    = COLORED(RAW, color = 'cyan', attrs = ['bold'])

# extension for zio
# write
def w(self, s): 
    self.write(s)

# writeline
def pr(self, *args): 
    if len(args) == 0:
        self.writeline()
    for stuff in args:
        if isinstance(stuff, (int, long)):
            self.writeline(str(stuff)) 
        elif isinstance(stuff, (list, tuple)): 
            self.writelines( [str(i) if isinstance(i, (int, long)) else i for i in stuff] )
        else:
            self.writeline(stuff)

# read
def r(self, size = None, timeout = -1):
    return self.read(size, timeout)

# readline
def rl(self, size = 1):
    return self.read_line(size)

# read_until
def ru(self, pattern_list, timeout = -1, searchwindowsize = None):
    return self.read_until(pattern_list, timeout, searchwindowsize)

def hint(self, breakpoints = None, relative = None, extras = None):
    self.gdb_hint(breakpoints, relative, extras)


# main
setattr(zio, 'w', w)
setattr(zio, 'pr', pr)
setattr(zio, 'r', r)
setattr(zio, 'rl', rl)
setattr(zio, 'ru', ru)
setattr(zio, 'hint', hint)

# utilities
def info_leak(arg1, arg2):
    print BLUE("[_] {} => {}".format(arg1, arg2))

def info_found(arg1, arg2):
    print GREEN("[+] {} :".format(arg1).ljust(0x20, ' ') + "{}".format(hex(arg2)))

def info_shell():
    print CYAN("\n[*] enjoy your shell ~")

def mk(target, debug = True):
    if debug:
        return zio(target, print_read = COLORED(REPR, 'red'), print_write = COLORED(REPR, 'yellow'), timeout = 10000)
    else:
        return zio(target, print_read = False, print_write = False, timeout = 10000)

__all__ = ['info_shell', 'info_leak', 'info_found', 'mk', 'stdout', 'log','l8', 'b8', 'l16', 'b16', 'l32', 'b32', 'l64', 'b64', 'zio', 'EOF', 'TIMEOUT', 'SOCKET', 'PROCESS', 'REPR', 'EVAL', 'HEX', 'UNHEX', 'BIN', 'UNBIN', 'RAW', 'NONE', 'COLORED', 'PIPE', 'TTY', 'TTY_RAW', 'cmdline']
