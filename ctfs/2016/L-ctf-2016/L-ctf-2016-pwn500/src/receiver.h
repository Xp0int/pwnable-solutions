typedef struct receiver {
    struct receiver *next;
    struct receiver *prev;
    char            receiver_name[0x10];
    char            receiver_postcodes[0x10];
    char            receiver_contact[0x10];
    package_ptr     package;
    char            receiver_address[0x40];
} receiver_strct, *receiver_ptr;

void insert_receiver_list(receiver_ptr *head_ptr, receiver_ptr node);
void delete_receiver_list(receiver_ptr *head_ptr, unsigned idx);
void show_receiver_list(receiver_ptr head);
unsigned len_receiver_list(receiver_ptr head);
receiver_ptr get_receiver_list(receiver_ptr head, unsigned idx);
