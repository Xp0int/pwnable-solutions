#include <stdio.h>
int main(int argc, const char *argv[])
{
    printf("\x10\x20\x60\x00\x00\x00\x00\x00.%6$016lx");
    return 0;
}
