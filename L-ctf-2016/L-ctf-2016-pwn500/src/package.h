typedef struct package {
    struct package  *next;
    struct package  *prev;
    unsigned long   length;
    char            payload[0x1f0];
} package_struct, *package_ptr;

void insert_package_list(package_ptr *head_ptr, package_ptr node);
void delete_package_list();
void destroy_package_list();
//package_ptr get_package_list(package_ptr head, unsigned idx);
