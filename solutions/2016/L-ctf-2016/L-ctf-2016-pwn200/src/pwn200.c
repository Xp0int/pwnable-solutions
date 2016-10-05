#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *sign = NULL;

void pre() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

int get_num() {
    int i = 0;
    int num = 0;
    char buf[4];
    for (i = 0; i < 0x4; i++) {
        read(0, &buf[i], 1);
        if (buf[i] == '\n') {
            buf[i] = '\x00';
            break;
        }
        else if (buf[i] > '9' || buf[i] < '0'){
            printf("0x%x ", buf[i]);
            return 0;
        }
    }
    num = atoi(buf);
    if (num < 0) {
        return 0;
    }
    return atoi(buf);
}

void new_sign(){
    if (!sign){
        int len;
        printf("how long?\n");
        len = get_num();
        if (len >0 && len <= 0x80) {
            sign = (char *)malloc(len);
            printf("give me more money : ");
            printf("\n%d\n", len);
            read(0, sign, len);
            printf("in~\n");
        }
        else {
            printf("invalid length\n");
            return;
        }
    }
    else {
        printf("already check in\n");
    }
}

void del_sign(){
    if (sign){
        printf("out~\n");
        free(sign);
        sign = NULL;
    }
    else {
        printf("havn't check in\n");
    }
}

void list_menu() {
    printf("\n=======EASY HOTEL========\n1. check in\n2. check out\n3. goodbye\nyour choice : ");
}

void select_menu() {
    int choice;
    while(1) {
        list_menu();
        choice = get_num();
        switch(choice){
            case 1:
                new_sign();
                break;
            case 2:
                del_sign();
                break;
            case 3:
                printf("good bye~\n");
                return;
            default:
                printf("invalid choice\n");
        }
    }
}

void entry() {
    char *stack_sign;
    char temp_sign[0x30];
    stack_sign = (char *)malloc(0x40);
    printf("give me money~\n");
    read(0, temp_sign, 0x40);                           // bug here
    strcpy(stack_sign, temp_sign);

    sign = stack_sign;

    select_menu();
}

void real_main() {
    printf("who are u?\n");
    char name[0x30];
    long i[2];
    char nop[0x10];
    for (*i = 0; *i < 0x30; *i = *i + 1) {
        read(0, &name[*i], 0x1);                         // bug here
        if (name[*i] == '\n') {
            name[*i] = '\x00';
            break;
        }
    }
    printf("%s, welcome to L-CTF~\n", name);

    printf("give me your id ~~?\n");
    i[1] = get_num();

    entry();
}

int main(int argc, const char *argv[])
{
    pre();
    real_main();
    return 0;
}
