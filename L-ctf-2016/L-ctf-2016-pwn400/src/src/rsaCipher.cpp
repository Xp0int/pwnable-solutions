#include "rsaCipher.h"
#include <cstdio>

RsaCipher::RsaCipher() {
    this -> keyChain = new KeyChain();
}

RsaCipher::~RsaCipher() {
}

void RsaCipher::printPT() {
    cout << "plaintext: " << this -> pt << endl;
}

void RsaCipher::printCT() {
    cout << "ciphertext: " << this -> ct << endl;
}

void RsaCipher::encrypt(char *pt, Key *pub) {
    unsigned ct[0x40];
    unsigned e=pub->getfirst();
    unsigned n=pub->getlast();
    unsigned len = this -> pt_len;
    unsigned char *ptr = (unsigned char *)ct;

    for (unsigned i = 0; i < len; i++) {
        this -> pt[i] = pt[i];
        ct[i] = powerwithmodule(pt[i],e,n);
    }

    for (unsigned i = 0; i < len*4; i++) {
        if (*ptr / 0x10 >= 0xa) {
            *(this -> ct + 2*i) = *ptr / 0x10 + 'a';
        }
        else if (*ptr / 0x10 < 0xa)  {
            *(this -> ct + 2*i) = *ptr / 0x10 + '0';
        }

        if (*ptr % 0x10 >= 0xa) {
            *(this -> ct + 2*i + 1) = *ptr % 0x10 + 'a';
        }
        else if (*ptr % 0x10 < 0xa) {
            *(this -> ct + 2*i + 1) = *ptr % 0x10 + '0';
        }
        ptr++;
        //sprintf(this -> ct + 2*i, "%02x", *((unsigned char *)ct + i));
    }
    this -> printCT();
}

void RsaCipher::encrypt(char *pt) {
    cout<<"I need public key!\n";
    unsigned e, n;
    cout<<"first number: ";
    cin>>e;
    cout<<"second number: ";
    cin>>n;
    Key *pub = new Key();
    pub->setfirst(e);
    pub->setlast(n);
    encrypt(pt,pub);
}

void RsaCipher::decrypt(char *ct, Key *priv) {
    unsigned d=priv->getfirst();
    unsigned n=priv->getlast();
    unsigned len = this -> pt_len;
    unsigned ct_int[0x40];
    unsigned char *ptr = (unsigned char *)ct_int;

    //for (unsigned i = 0; i < len*4; i++) {
    //    this -> ct[i] = ct[i];
    //    sscanf((ct + 2*i), "%02x", (unsigned char *)ct_int + i);
    //}

    for (unsigned i = 0; i < 4*len; i++) {
        if (ct[2*i] >= 'a' && ct[2*i] <= 'f') {
            ptr[i] = (ct[2*i] - 'a' + '0' + 10) * 0x10;
        }
        else {
            ptr[i] = (ct[2*i] - '0') * 0x10;
        }
        if (ct[2*i+1] >= 'a' && ct[2*i+1] <= 'f') {
            ptr[i] += ct[2*i+1] - 'a' + '0' + 10;
        }
        else {
            ptr[i] += ct[2*i+1] - '0';
        }
    }

    for (unsigned i = 0; i < len; i++) {
        this -> pt[i] = powerwithmodule(ct_int[i],d,n);
    }
    this -> printPT();
}

void RsaCipher::decrypt(char *ct) {
    cout<<"I need private key!\n";
    unsigned d, n;
    cout<<"first number: ";
    cin>>d;
    cout<<"second number: ";
    cin>>n;
    Key *pr=new Key(d,n);
    cout<<"Your key:\t";
    pr->print();
    decrypt(ct, pr);
}
