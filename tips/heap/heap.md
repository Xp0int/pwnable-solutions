### 0x1 Tech
1. [Malloc Maleficarum](https://sploitfun.wordpress.com/2015/03/04/heap-overflow-using-malloc-maleficarum/)
2. unsorted bin unlink (free'd)
3. small/large bin unlink (malloc'd)
4. fastbin duplicate
5. hijack function pointer
6. [craft overlapping chunks](https://www.contextis.com/documents/120/Glibc_Adventures-The_Forgotten_Chunks.pdf)
7. heap spray

#### 0x11 Malloc Maleficarum
##### house of force
> 1. control heap chunk pointer
> 2. leak stack address
##### house of spirit
> 1. leak heap address
> 2. heap overflow to `top_chunk -> size`
> 3. malloc'd size can be controlled by attacker
##### house of lore
> 1. leak heap address
> 2. heap overflow

#### 0x12 unsorted bin unlink (free'd)
**DWORD shoot** while **unlink** of unsorted bin 

#### 0x13 small/large bin unlink (malloc'd)
**DWORD shoot** while **unlink** of small/large bin.

#### 0x14 fastbin duplicate

#### 0x15 hijack function pointer
Followed by **ROP**

#### 0x16 craft overlapping chunks
> 1. double free
> 2. hijack function pointer

1. shrink free chunks
2. extend free chunks
3. extend allocated chunks

#### 0x17 heap spray
[To Be Finished] 

### 0x2 Vulns
1. double free
2. use after free
3. heap overflow
4. off by one

#### 0x21 double free
unsorted bin unlink (free'd)
fastbin duplicate

#### 0x22 use after free
hijack function pointer => rop (C++)

#### 0x23 heap overflow
unsorted bin unlink (free'd)
small/large bin unlink (malloc'd) | house of lore
fastbin duplicate

#### 0x24 off by one
unsorted bin unlink (free'd)
overlapping chunks
