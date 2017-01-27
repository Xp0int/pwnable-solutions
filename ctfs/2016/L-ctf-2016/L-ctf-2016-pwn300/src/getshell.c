typedef long long int64;

void getshell() {
    asm(
            "xor %%eax, %%eax\n"
            "mov $0xFF978CD091969DD1, %%rbx\n"
            "neg %%rbx\n"
            "push %%rbx\n"
            "push %%rsp\n"
            "pop %%rdi\n"
            "cdq\n"
            "push %%rdx\n"
            "push %%rdi\n"
            "push %%rsp\n"
            "pop %%rsi\n"
            "mov $0x3b, %%al\n"
            "syscall\n"
            :::
       );

}

void this_is_not_flag_run_will_exit() {
    asm(
            "mov $60, %%rax\n"
            "mov $0x0, %%rdi\n"
            "syscall"
            ::: 
       );
}
