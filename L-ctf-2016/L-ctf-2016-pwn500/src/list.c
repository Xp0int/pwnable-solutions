#include <stdio.h>
#include "list.h"
/*
 * list menus
 */
void list_receiver() {
    //printf("\n======= Packages Log ========\n1. set receiver info\n2. new a package\n3. edit a package\n4. delete a package\n5. show packages\n6. save packages\n7. exit\nyour choice : ");
    printf("\n======= Packages Log ========\n1. set receiver info\n2. new a package\n3. delete a package\n4. show packages\n5. save packages\n6. exit\nyour choice : ");
}

void list_sender() {
    printf("\n======= Receivers Log ========\n1. set sender info\n2. new a receiver\n3. edit a receiver\n4. delete a receiver\n5. show all receivers\n6. submit all packages\n7. exit\nyour choice : ");
}

void list_main() {
    printf("\n======= XDSEC Compress Station =======\nsend packages(y or n)?\n");
}
