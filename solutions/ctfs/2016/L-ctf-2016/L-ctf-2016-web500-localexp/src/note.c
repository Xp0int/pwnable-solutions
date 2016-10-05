#include <stdio.h>

void vuln() {
    char note[0x20];
    puts("take notes here~");
    read(0, note, 0x2c); 
}

void prev() {
}

int main(int argc, const char *argv[], char **envp)
{
    char*** pargv = &argv;
    char*** penvp = &envp;
    char** arg;
    char* c;
    for(arg=argv;*arg;arg++) for(c=*arg; *c;c++) *c='\0';
    for(arg=envp;*arg;arg++) for(c=*arg; *c;c++) *c='\0';
    *pargv=0;
    *penvp=0;

    vuln();
    return 0;
}
