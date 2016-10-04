#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "package.h"
#include "receiver.h"
#include "sender.h"
#include "gadget.h"

/*
 * (package_ptr)malloc(0x208)
 * (receiver_ptr)malloc(0xc8)
 * (sender_ptr)malloc(0x98)
 */

typedef struct _control {
    receiver_ptr    receiver_head;
    sender_ptr      sender_head;
    package_ptr     package_head;
} *control_ptr;

control_ptr control; 

/*
 * receiver
 */
receiver_ptr info_receiver() {
    receiver_ptr receiver_temp = (receiver_ptr)malloc(0xb8);
    receiver_temp -> next = NULL;
    receiver_temp -> prev = NULL;

    printf("your name?\n");
    get_str(receiver_temp -> receiver_name, 0x8, '\n');

    printf("your postcodes?\n");
    get_str(receiver_temp -> receiver_postcodes, 0x8, '\n');

    printf("your contact?\n");
    get_str(receiver_temp -> receiver_contact, 0x8, '\n');

    printf("your address?\n");
    get_str(receiver_temp -> receiver_address, 0x38, '\n');

    return receiver_temp;
}

void new_package(receiver_ptr receiver_temp) {
    if (receiver_temp == NULL) {
        printf("give receiver's info first~");
        return;
    }
    unsigned len = 0;

    printf("length of your package?\n");
    len = get_num();
    if (len > 0x1f0) {
        printf("too long!\n");
        return;
    }

    package_ptr package_temp = (package_ptr)malloc(len + 0x18);
    package_temp -> prev = NULL;
    package_temp -> next = NULL;
    package_temp -> length = len;

    printf("input your package~\n");
    get_str(package_temp -> payload, len, '\n');

    insert_package_list(&(control -> package_head), package_temp);
}

// void edit_package(receiver_ptr receiver_temp) {
//     package_ptr package_temp;
//     char buf[0x200];
//     if (receiver_temp == NULL) {
//         printf("give receiver's info first~");
//         return;
//     }
//     unsigned index;
//     unsigned length = len_package_list(control -> package_head);
//     if (length == 0) {
//         printf("new a package first\n");
//         return;
//     }
//     printf("index of package that you want to edit?\n");
//     index = get_num();
//     if (index >= length) {
//         printf("invalid index\n");
//     }
//     else {
//         package_temp = get_package_list(control -> package_head, index);
//         get_str(buf, package_temp -> length, '\n');
//         strcpy(package_temp -> payload, buf);
//         printf("edit successfully\n");
//     }
// }

void delete_package(receiver_ptr receiver_temp) {
    if (receiver_temp == NULL) {
        printf("give receiver's info first~");
        return;
    }
    unsigned index;
    unsigned length = len_package_list(control -> package_head);
    if (length == 0) {
        printf("new a package first\n");
        return;
    }
    printf("index of package that you want to delete?\n");
    index = get_num();
    if (index >= length) {
        printf("invalid index\n");
    }
    else {
        delete_package_list(&(control -> package_head), index);
        printf("delete successfully\n");
    }
}

void show_packages(receiver_ptr receiver_temp) {
    if (receiver_temp == NULL) {
        printf("give receiver's info first~");
        return;
    }
    show_package_list(control -> package_head);
}

void save_packages(receiver_ptr receiver_temp) {
    if (receiver_temp == NULL) {
        printf("give receiver's info first~");
        return;
    }
    if (control -> package_head) {
        receiver_temp -> package = control -> package_head;
    }
    insert_receiver_list(&(control -> receiver_head), receiver_temp);
    // bug here 
    // free(receive_temp);
    // package_head = NULL;
}

/*
 * sender
 */
sender_ptr info_sender() {
    sender_ptr sender_temp = (sender_ptr)malloc(0x98);
    control -> sender_head = sender_temp;

    printf("your name?\n");
    get_str(sender_temp -> sender_name, 0x8, '\n');

    printf("your contact?\n");
    get_str(sender_temp -> sender_contact, 0x18, '\n');

    return sender_temp;
}

void edit_receiver(sender_ptr sender_temp) {
    receiver_ptr receiver_temp;
    char name[0x10];
    char postcodes[0x10];
    char contact[0x10];
    char address[0x40];

    if (sender_temp == NULL) {
        printf("give receiver's info first~");
        return;
    }
    unsigned index;
    unsigned length = len_receiver_list(control -> receiver_head);
    if (length == 0) {
        printf("new a receiver first\n");
        return;
    }
    printf("index of receiver that you want to edit?\n");
    index = get_num();
    if (index >= length) {
        printf("invalid index\n");
    }
    else {
        printf("your name?\n");
        get_str(name, 0x8, '\n');

        printf("your postcodes?\n");
        get_str(postcodes, 0x8, '\n');

        printf("your contact?\n");
        get_str(contact, 0x8, '\n');

        printf("your address?\n");
        get_str(address, 0x38, '\n');

        receiver_temp = get_receiver_list(control -> receiver_head, index);
        strcpy(receiver_temp -> receiver_name, name);
        strcpy(receiver_temp -> receiver_postcodes, postcodes);
        strcpy(receiver_temp -> receiver_contact, contact);
        strcpy(receiver_temp -> receiver_address, address);
        printf("edit successfully\n");
    }
}

void delete_receiver(sender_ptr sender_temp) {
    if (sender_temp == NULL) {
        printf("give sender's info first~");
        return;
    }
    unsigned index;
    unsigned length = len_receiver_list(control -> receiver_head);
    if (length == 0) {
        printf("new a receiver first\n");
    }
    printf("index of receiver that you want to delete?\n");
    index = get_num();
    if (index >= length) {
        printf("invalid index\n");
    }
    else {
        delete_receiver_list(&(control -> receiver_head), index);
        printf("delete successfully\n");
    }
}

void show_receivers(sender_ptr sender_temp) {
    if (sender_temp == NULL) {
        printf("give your info first~\n");
        return;
    }
    show_receiver_list(control -> receiver_head);
}

void submit_packages(sender_ptr sender_temp) {
    if (sender_temp == NULL) {
        printf("give your info first~\n");
        return;
    }
    control -> package_head = NULL;
    control -> receiver_head = NULL;
    free(sender_temp);
}

void menu_receiver(sender_ptr sender_temp) {
    if (sender_temp == NULL) {
        printf("give your info first~\n");
        return;
    }
    int choice;
    receiver_ptr receiver_temp = NULL;
    while(1) {
        list_receiver();
        choice = get_num();
        switch(choice){
            case 1:
                receiver_temp = info_receiver();
                break;
            case 2:
                new_package(receiver_temp);
                break;
//            case 3:
//                edit_package(receiver_temp);
//                break;
            case 3:
                delete_package(receiver_temp);
                break;
            case 4:
                show_packages(receiver_temp);
                break;
            case 5:
                save_packages(receiver_temp);
                if (receiver_temp) {
                    return;
                }
                break;
            case 6:
                control -> package_head = NULL;
                return;
            default:
                printf("invalid choice\n");
        }
    }
}

void menu_sender() {
    int choice;
    sender_ptr sender_temp = NULL;
    while(1) {
        list_sender();
        choice = get_num();
        switch(choice){
            case 1:
                sender_temp = info_sender();
                break;
            case 2:
                menu_receiver(sender_temp);
                break;
            case 3:
                edit_receiver(sender_temp);
                break;
            case 4:
                delete_receiver(sender_temp);
                break;
            case 5:
                show_receivers(sender_temp);
                break;
            case 6:
                submit_packages(sender_temp);
                sender_temp = NULL;
                break;
            case 7:
                control -> receiver_head = NULL;
                sender_temp = NULL;
                return;
            default:
                printf("invalid choice\n");
        }
    }
}

void menu_main() {
    char choice;
    while(1) {
        list_main();
        scanf("%c", &choice);
        getchar();
        if (choice == 'y') {
            menu_sender();
        }
        else if (choice == 'n') {
            printf("it's time to go home :(\n");
            return;  
        }
        else {
            printf("invalid choice\n");
        }
    }
}

void init_control() {
    control = (control_ptr) malloc(0x20);
    control -> sender_head      = NULL;
    control -> receiver_head    = NULL;
    control -> package_head     = NULL;
}

int main(int argc, const char *argv[])
{
    cancel_io_buf();
    init_control();
    menu_main();
    return 0;
}
