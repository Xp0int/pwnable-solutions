from zio import *

target  = './shaxian_51f320b11793463ecdcfbb0c015cc273'

c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')

io      = zio(target, print_read = c_read, print_write = c_write)

def diancai(idx, num):
    io.read_until('choose:')
    io.writeline('1')

    io.read_until('5.Jianjiao')
    io.writeline(str(idx))

    io.read_until('How many?')
    io.writeline(str(num))

def submit():
    io.read_until('choose:')
    io.writeline('2')

def submit():
    io.read_until('choose:')
    io.writeline('3')

def submit():
    io.read_until('choose:')
    io.writeline('4')
    
io.read_until('Your Address:')
io.writeline('xdsec')

io.read_until('Your Phone number:')
io.writeline('110')

diancai()

io.interact()
