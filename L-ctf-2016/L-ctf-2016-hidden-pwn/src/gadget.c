#include <stdio.h>

/*
 * gadgets
 */
void cancel_io_buf() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

/*
 * bug here; off-by-one
 */
void get_str(char *buf, unsigned int length, char ch) {
    int i = 0;
    for (i = 0; i < length - 1; i++) {
        read(0, &buf[i], 1);
        if (buf[i] == '\n') {
            buf[i] = '\x00';
            break;
        }
    }
    buf[i] = '\x00';
}

int get_num() {
    int i = 0;
    int val = 0;
    char buf[4];
    get_str(buf, 4, '\n');
    val = atoi(buf);
    if (val < 0) {
        return 0;
    }
    return atoi(buf);
}

void print_and_get_str(char *str, char *buf, unsigned int length, char ch) {
    printf("%s", str);
    get_str(buf, length, ch);
}

unsigned print_and_get_num(char *str) {
    printf("%s", str);
    return get_num();
}
