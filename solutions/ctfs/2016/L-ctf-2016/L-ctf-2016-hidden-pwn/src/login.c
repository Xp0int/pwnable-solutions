#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "md5.h"
#include "base64.h"

char md5_enc[] = "d429a66f3e16481c7cf7b0e404096fd9";
void compare(char *str, int str_len) {
    int i = 0;
    int len = strlen(md5_enc);
    char *md5_dec = (char *)malloc(0x20);
    int flag = 1;
    for (i = 0; i < len/2; i++) {
        if (md5_enc[2*i] >= 'a' && md5_enc[2*i] <= 'f') {
            md5_enc[2*i] = md5_enc[2*i] - 'a' + '0' + 10;
        }
        if (md5_enc[2*i+1] >= 'a' && md5_enc[2*i+1] <= 'f') {
            md5_enc[2*i+1] = md5_enc[2*i+1] - 'a' + '0' + 10;
        }
        md5_dec[i] = ((md5_enc[2*i] - '0') * 0x10 + (md5_enc[2*i+1] - '0')) ^ (i+1);
    }

    for (i = 0; i < str_len; i++) {
        if (md5_dec[i] != str[i]) {
            flag = 0;
            break;
        } 
    }

    if (flag) {
        printf("login!\n");
    }
    else {
        printf("error!\n");
        exit(1);
    }
}

void login() {
    int i = 0;
    char pt[0x20];
    scanf("%32s", pt);
    char *pt_b64_decode;
    char *digest = (char *)malloc(0x20);
    pt_b64_decode = b64_decode(pt, strlen(pt));
    md5(pt_b64_decode, strlen(pt_b64_decode), digest);
    compare(digest, strlen(digest));
}
