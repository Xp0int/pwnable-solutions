typedef struct tuple {
    struct tuple    *next;
    struct tuple    *prev;
    unsigned        id;
    unsigned        type;
    char            name[0x10];
    char            description[0x60];
    unsigned        canary;
} tuple_struct, *tuple_ptr;

tuple_ptr get_tuple_list(tuple_ptr head, unsigned idx);
char *serial_tuple_list(tuple_ptr *head, unsigned idx, unsigned length);
