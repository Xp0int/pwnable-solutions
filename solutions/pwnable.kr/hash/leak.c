#include <stdio.h>

int main(int argc, const char *argv[])
{
    int i = 0;
    int a[8];
    srand(atoi(argv[1]));
    for(; i < 8; i++){
        a[i] = rand();
        printf("%d*", a[i]);
    }
    puts("");
    return 0;
}
