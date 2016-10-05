#include <iostream>
#include <cmath>
#include <cstdio>
#include <unistd.h>

#include "rsamath.h"
#include "key.h"
#include "rsaCipher.h"

using namespace std;

RsaCipher *cipher;

void get_str(char *buf, unsigned int length, char ch) {
    int i = 0;
    for (i = 0; i < length; i++) {
        read(0, &buf[i], 1);
        if (buf[i] == '\n') {
            buf[i] = '\x00';
            break;
        }
    }
    if (i == length) {
        buf[i-1] = '\x00';
    } 
}

int main(){
    int a;
    Key *pub, *priv;
    KeyChain *chain;
    unsigned len;
    cout<<"RSA example"<<endl;

    setbuf(stdin, 0);
    setbuf(stdout, 0);

    while (1) {

        cout<<"What do you want to do?\n";
        cout<<"1. new cipher\n2. encrypt\n3. decrypt\n4. comment\n5. exit\n";
        cin>>a;
        switch(a){
            case 1:
                cipher = new RsaCipher();
                chain = cipher -> getKeyChain();

                if(chain->isready()){
                    pub=chain->getpub();
                    priv=chain->getpriv();	
                    chain->print();
                }
                break;
            case 2:
                if (cipher) {
                    cout << "length of your plaintext (max: 0x40)" << endl;
                    cin >> len;
                    if (len > 0x40) {
                        cout << "invalid length";
                        break;
                    }
                    cipher -> setPtLen(len);
                    cout << "write your plaintext" << endl;
                    char pt[0x40];
                    get_str(pt, len, '\x00');
                    chain->isready() ? cipher -> encrypt(pt, pub) : cipher -> encrypt(pt);
                }
                else {
                    cout << "new a cipher first" << endl;
                }
                break;
            case 3:
                if (cipher) {
                    cout << "length of your ciphertext (max: 0x200, hex encoded)" << endl;
                    cin >> len;
                    if (len > 0x100) {
                        cout << "invalid length";
                        break;
                    }
                    cipher -> setPtLen(len/4);
                    cout << "write your ciphertext" << endl;
                    char ct[0x200];
                    get_str(ct, len*2, '\x00');
                    chain->isready() ? cipher -> decrypt(ct, priv) : cipher -> decrypt(ct);
                    delete cipher;  // bug here
                }
                else {
                    cout << "new a cipher first" << endl;
                }
                break;
            case 4: {
                printf("comment about my implement of RSA") ;
                char *comment = new char[0x80];
                get_str(comment, 0x80, '\x00');
                break;
            }
            case 5:
                cout << "bye~";
                return 0;
            default:
                cout << "invalid"<< endl;
                break;
        }

    }
    return 0;
}
