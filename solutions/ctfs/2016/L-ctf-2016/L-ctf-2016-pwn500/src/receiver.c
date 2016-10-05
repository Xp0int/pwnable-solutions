#include <stdio.h>
#include <stdlib.h>
#include "package.h"
#include "receiver.h"

/*
 * gadget
 */
void insert_receiver_list(receiver_ptr *head_ptr, receiver_ptr node) {
    receiver_ptr head = *head_ptr;
    if (head != NULL) {
        node -> prev = NULL;
        node -> next = head;
        head -> prev = node;
        *head_ptr = node;
    }
    else {
        node -> next = NULL;
        node -> prev = NULL;
        *head_ptr = node;
    }
}

receiver_ptr get_receiver_list(receiver_ptr head, unsigned idx) {
    receiver_ptr temp = head;
    int i = 0;
    if (!(head)) {
        printf("no receiver\n");
        return ;
    }

    if (idx == 0) {
        return head;
    }

    for (i = 0; i < idx; i++) {
        temp = temp -> next;
    }
    return temp;
}

void delete_receiver_list(receiver_ptr *head_ptr, unsigned idx) {
    receiver_ptr head = *head_ptr;
    receiver_ptr temp = head;
    receiver_ptr prev;
    receiver_ptr next;
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

void show_receiver_list(receiver_ptr head) {
    int idx = 0;
    receiver_ptr temp = head;
    if (head) {
        while(1) {
            printf("\n======receiver[%d]=======\nname:%s\npostcodes:%s\ncontact:%s\naddress:%s\n", idx, temp -> receiver_name, temp -> receiver_postcodes, temp -> receiver_contact, temp -> receiver_address);
            temp = temp -> next;
            idx++;
            if (temp == NULL) {
                break;
            }
        }
    }
    else {
        printf("no receiver:(\n");
    }
}

unsigned len_receiver_list(receiver_ptr head) {
    unsigned idx = 0;
    receiver_ptr temp = head;
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
