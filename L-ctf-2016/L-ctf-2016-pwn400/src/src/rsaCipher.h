#ifndef RSAOPS_H
#define RSAOPS_H

#include "key.h"
#include "rsamath.h"

class RsaCipher {
    private:
        char        pt[0x40];   // any character
        char        ct[0x200];  // 1 to 1
        KeyChain    *keyChain;

        unsigned    pt_len;
        void printCT();
        void printPT();
    public:
        RsaCipher();
        virtual ~RsaCipher();
        void setPtLen(unsigned len) {this -> pt_len = len;};
        KeyChain *getKeyChain() {return this -> keyChain;};
        virtual void encrypt(char *pt, Key *pub);       // secret size  : 0x40
        virtual void encrypt(char *pt);                 // secret size  : 0x40
        virtual void decrypt(char *ct, Key *priv);     // message size : 0x200
        virtual void decrypt(char *ct);                // message size : 0x200
};
#endif
