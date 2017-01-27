#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void readstr(char *str, int len, char ch) {
    int i = 0;
    for(i = 0; i < len; ++i) {
        read(0, &str[i], 1);
    }
}

void vuln() {
    char msg[0x40];

    readstr(msg, 0xc8, '\n');
    puts("bye~");
}

int main(int argc, char const *argv[])
{
    //set I/O buff

    setbuf(stdin, 0);
    setbuf(stdout, 0);

    vuln();
    return 0;
}

