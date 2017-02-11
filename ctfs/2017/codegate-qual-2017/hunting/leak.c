#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, const char *argv[])
{
    int i = 0;
    int a;
    int layout = atoi(argv[1]);
    printf("%d\n", time(0) + layout);
    srand(time(0) + layout);

    for (int i = 0; i < 0x10000; i++) {
            a = rand();
            printf("%d\n", a);
    }
    return 0;
}
