#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tuple.h"

/*
 * gadget
 */
void insert_tuple_list(tuple_ptr *head_ptr, tuple_ptr node) {
    tuple_ptr head = *head_ptr;
    tuple_ptr temp;
    tuple_ptr prev;
    tuple_ptr next;
    if (head != NULL) {
        temp = head;
        while (1) {
            if (temp -> id >= node -> id) {
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

void delete_tuple_list(tuple_ptr *head_ptr, unsigned idx) {
    tuple_ptr head = *head_ptr;
    tuple_ptr temp = head;
    tuple_ptr prev;
    tuple_ptr next;
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

tuple_ptr get_tuple_list(tuple_ptr head, unsigned idx) {
    tuple_ptr temp = head;
    int i = 0;
    if (!(head)) {
        printf("no tuple:(\n");
    }

    if (idx == 0) {
        return head;
    }

    for (i = 0; i < idx; i++) {
       temp = temp -> next;
    }
    return temp;
}

void show_tuple_list(tuple_ptr head) {
    int idx = 0;
    tuple_ptr temp = head;
    if (head) {
        while(1) {
            printf("\n======= bomb [%d]=======\nid:%u\tname:%s\ndescription:%s\n", idx, temp -> id, temp -> name, temp -> description);
            temp = temp -> next;
            idx++;
            if (temp == NULL) {
                break;
            }
        }
    }
    else {
        printf("no tuple:(\n");
    }
}

unsigned len_tuple_list(tuple_ptr head) {
    unsigned idx = 0;
    tuple_ptr temp = head;
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
char *serial_tuple_list(tuple_ptr *head, unsigned idx, unsigned length) {
    tuple_ptr temp = *head;
    char name[0x10];
    char description[0x60];
    char *serial = (char *)malloc(0x1d0);
    tuple_ptr node;
    int i = 0;
    if (!(temp)) {
        printf("no tuple\n");
        return NULL;
    }

    for (i = 0; i < idx; i++) {
        if (i == 0) {
            break;
        }
        temp = temp -> next;
    }

    *((unsigned *)serial) = temp -> id;
    *((unsigned *)serial+1) = temp -> type;
    strcpy(serial + 0x8, temp -> name);
    strcpy(serial + 0x8, temp -> description);
    printf("serial: ");
    for (i = 0; i < 0x1d0; i++) {
        printf("%02x", (unsigned)serial[i]);
    }
    return serial;
}
int check_tuple_list(tuple_ptr node, unsigned canary) {
    if (node -> canary != canary) {
        printf(":(");
        exit(1);
    }
}
