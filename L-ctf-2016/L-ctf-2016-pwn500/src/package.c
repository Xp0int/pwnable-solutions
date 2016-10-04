#include <stdio.h>
#include <stdlib.h>
#include "package.h"

/*
 * gadget
 */
void insert_package_list(package_ptr *head_ptr, package_ptr node) {
    package_ptr head = *head_ptr;
    package_ptr temp;
    package_ptr prev;
    package_ptr next;
    if (head != NULL) {
        temp = head;
        while (1) {
            if (temp -> length >= node -> length) {
                prev = temp -> prev;
                if (!prev) {
                    temp -> prev = node;
                    node -> next = temp;
                    *head_ptr = node;
                    break;
                }
                prev -> next = node;
                temp -> prev = node;
                node -> prev = prev;
                node -> next = temp;
                break;
            }
            if (temp -> next == NULL) {
                temp -> next = node;
                node -> next = NULL;
                node -> prev = temp;
                break;
            }
            temp = temp -> next;
        }
    }
    else {
        node -> next = NULL;
        node -> prev = NULL;
        *head_ptr = node;
    }
}

void delete_package_list(package_ptr *head_ptr, unsigned idx) {
    package_ptr head = *head_ptr;
    package_ptr temp = head;
    package_ptr prev;
    package_ptr next;
    int i = 0;
    if (idx == 0) {
        *head_ptr = head -> next;
        if (head -> next) {
            head -> next -> prev = NULL;
        }
        free(head);
        return;
    }
    for (i = 0; i < idx; i++) {
       temp = temp -> next;
    }

    if (temp -> next == NULL) {
        prev = temp -> prev;
        prev -> next = NULL;
        free(temp);
    }
    else {
        prev = temp -> prev;
        next = temp -> next;
        prev -> next = next;
        next -> prev = prev;
        free(temp);
    }
}

// package_ptr get_package_list(package_ptr head, unsigned idx) {
//     package_ptr temp = head;
//     int i = 0;
//     if (!(head)) {
//         printf("no package:(\n");
//     }
// 
//     if (idx == 0) {
//         return head;
//     }
// 
//     for (i = 0; i < idx; i++) {
//        temp = temp -> next;
//        i++;
//     }
//     return temp;
// }

void show_package_list(package_ptr head) {
    int idx = 0;
    package_ptr temp = head;
    if (head) {
        while(1) {
            printf("\n=======pack[%d]=======\nlength:%lu\tcontent:%s\n", idx, temp -> length, temp -> payload);
            temp = temp -> next;
            idx++;
            if (temp == NULL) {
                break;
            }
        }
    }
    else {
        printf("no package:(\n");
    }
}

unsigned len_package_list(package_ptr head) {
    unsigned idx = 0;
    package_ptr temp = head;
    if (head) {
        while(1) {
            temp = temp -> next;
            idx++;
            if (temp == NULL) {
                break;
            }
        }
    }
    return idx;
}
