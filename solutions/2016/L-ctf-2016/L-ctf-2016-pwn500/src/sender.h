typedef struct sender_info {
    char            sender_name[0x10];
    char            sender_contact[0x30];
    receiver_ptr    receiver;
} sender_struct, *sender_ptr;
