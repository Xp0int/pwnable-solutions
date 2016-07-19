from zio import *

target  = ('pwnable.kr', 9007)
c_read  = COLORED(RAW, 'green')
c_write = COLORED(RAW, 'blue')
io      = zio(target, print_read = c_read, print_write = c_write, timeout=1000)

io.read_until('- Ready? starting in 3 sec... -')

def read_title():
    io.read_until('N=')
    num     = int(io.read_until('C=')[0:-3])
    chance  = int(io.read_until('\n')[0:-1])
    return (num,chance)

def test(frm, to):
    num = to - frm + 1
    a = (num + 1)/2
    payload1 = ''

    for i in range(0, a-1):
        payload1 += (str(frm + i) + ' ')
    payload1 += str(frm + a - 1)
    io.writeline(payload1)
    value1 = int(io.read_line())

    if value1 < a * 10:
        return 0
    else:
        return 1

def solve(title):
    a = 0
    b = title[0] - 1
    while a != b :
        judge = test(a, b)
        if judge:
            a = (b - a + 2)/2 + a
        else:
            b = (b - a + 2)/2 + a - 1
        print 'a:'+str(a)+' b:'+str(b)
    io.writeline(str(a))

for i in range(0, 100):
    solve(read_title())
    io.read_until('Correct!')

io.interact()
