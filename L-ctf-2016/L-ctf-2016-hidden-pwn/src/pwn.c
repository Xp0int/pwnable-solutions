#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "gadget.h"
#include "base64.h"
#include "md5.h"
#include "tuple.h"

typedef struct _head {
    tuple_ptr   tuple;
    char        *serial;
} *head_ptr;


struct {
    char fake[0x40];
    head_ptr head;
    unsigned canary;
    long id;
} global_data;


void add() {
    unsigned type;
    char name[0x10];
    char description[0x60];
    type = print_and_get_num("----type----\n1. small\n2. middle\n3. large\nchoice? ");
    tuple_ptr node = (tuple_ptr)malloc(0xb0);
    node -> type = type;
    node -> canary = global_data.canary;
    print_and_get_str("\nname? ", node -> name, 0x10, '\n');
    print_and_get_str("\ndescription? ", node -> description, 0x58, '\n');
    node -> id = global_data.id;
    insert_tuple_list(&(global_data.head -> tuple), node);
    global_data.id++;
    //check_tuple_list(head -> tuple, canary);
}

void del() {
    unsigned choice;
    choice = print_and_get_num("index of bomb you want to delete? ");
    if (len_tuple_list(global_data.head -> tuple) > choice)
        delete_tuple_list(&(global_data.head -> tuple), choice);
    //check_tuple_list(head -> tuple, canary);
}

void mod() {
    unsigned type;
    unsigned idx;
    char name[0x10];
    char description[0x60];
    tuple_ptr node;

    idx = print_and_get_num("index of bomb you want to modify?");
    if (len_tuple_list(global_data.head -> tuple) > idx) {
        type = print_and_get_num("----type----\n1. small\n2. middle\n3. large\nchoice? ");
        node = (tuple_ptr)get_tuple_list(global_data.head -> tuple, idx);
        print_and_get_str("\nname? ", node -> name, 0x10, '\n');
        print_and_get_str("\ndescription? ", node -> description, 0xc0, '\n');
        node -> type = type;
        check_tuple_list(node, global_data.canary);
    }
    else {
        printf("invalid choice");
    }
}

void list() {
    show_tuple_list(global_data.head -> tuple);
    //check_tuple_list(head -> tuple, canary);
}

void serial() {
    unsigned idx = print_and_get_num("index of bomb you want to serialize?");
    char *serial_ptr;
    if (len_tuple_list(global_data.head -> tuple) > idx) {
        serial_ptr = (char *)serial_tuple_list(&(global_data.head -> tuple), idx, len_tuple_list(global_data.head -> tuple));

    }
    else {
        printf("invalid choice");
    }
}

void list_menu() {
    printf("====== XDSEC ======\n1. add a bomb\n2. delete a bomb\n3. modify a bomb\n4. list all bombs\n5. generate serial\nchoice? ");
}

void select_menu() {
    while(1) {
        list_menu();
        unsigned choice = get_num();
        switch(choice) {
            case 1:
                add();
                break;
            case 2:
                del();
                break;
            case 3:
                mod();
                break;
            case 4:
                list();
                break;
            case 5:
                serial();
                break;
            default:
                break;
        }
    }
}

void useless_print() {
    printf("===== XDSEC nuclear bomb expriment =====\n");
}

void initial() {
    int i = 0;
    char buf[0x28];

    srand(time(0));
    global_data.canary = random();
    *(head_ptr *)(&buf[0x20]) = (head_ptr)malloc(0x10);    
    printf("your id?");
    for(i = 0; i < 0x20; i++) {
        read(0, &buf[i], 1);
        if (buf[i] == '\n') {
            buf[i] = '\x00';
            break;
        }
    }
    printf("%s, begin your nuclear bomb expriment", buf);
    global_data.head = *(head_ptr *)(&buf[0x20]);
}

int main(int argc, const char *argv[]) {
    cancel_io_buf();
    login();
    initial();
    printf("\nhello? ");
    scanf("%64s", global_data.fake);
    useless_print();   
    select_menu();
    return 0;
}
