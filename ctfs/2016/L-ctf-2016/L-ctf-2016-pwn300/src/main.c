void gadget() {
    asm(
        "mov    %%r13,%%rdx\n"      
        "mov    %%r14,%%rsi\n"
        "mov    %%r15d,%%edi\n"
        "callq  *(%%r12,%%rbx,8)\n"
        "add    $0x1,%%rbx\n"
        "cmp    %%rbp,%%rbx\n"
        "add    $0x8,%%rsp\n"
        "pop    %%rbx\n"
        "pop    %%rbp\n"
        "pop    %%r12\n"
        "pop    %%r13\n"
        "pop    %%r14\n"
        "pop    %%r15\n"
        "retq"
         :::
        );
}

int main() {
    char buf[0x20];

    // print
    write(1, "fuck me!\n", 9);

    // read
    read(0, buf, 0xa0);

    return 0;
}

void _start() {
    exit(main());
}

void test() {
    this_is_not_flag_run_will_exit();
}
