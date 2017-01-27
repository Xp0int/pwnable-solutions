#include <stdio.h>

int main(int argc, const char *argv[])
{
    int i = 0;
    int a;
    srand(atoi(argv[1]));
    a = rand();
    printf("%d\n", a);
    return 0;
}
