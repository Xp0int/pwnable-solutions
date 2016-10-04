#include "key.h"
#include "rsamath.h"
#include <stdlib.h>

KeyChain::KeyChain(){
    unsigned p, q;
    unsigned a;
    cout<<"already have a keychain?\n";
    do{
        cout<<"[0]Yes\n[1]No\n";
        cin>>a;
    }while(a!=0&&a!=1);
    switch(a){
        case 1:
            do{
                cout<<"give me a prime number p: "<<endl;
                cin>>p;  
                if(!is_prime(p)) cout<<"it should be prime!\n";
            }while(!is_prime(p));

            do{
                cout<<"give me a prime number q: "<<endl;
                cin>>q;  
                if(!is_prime(q)||q==p) cout<<"it should be prime and differ from "<<p<<"!\n";
            }while(!is_prime(q)||q==p);	
            ready=true;
            break;
        case 0:
            ready=false;
            break;
    }

    generate_keypair(p,q);
}

void KeyChain::generate_keypair(const  unsigned &p, const unsigned &q){
    unsigned n=p*q;
    unsigned phi=(p-1)*(q-1);
    unsigned e,d;
    do{
        e=rand()%phi+1;
        d=multiplicative_inverse(e,phi);
    }while(!are_coprime(e,phi)||d==e);
    priv.setfirst(e);
    priv.setlast(n);
    pub.setfirst(d);
    pub.setlast(n);
    return;
}

unsigned KeyChain::multiplicative_inverse( unsigned e,  unsigned phi){
    unsigned d = 0;
    unsigned x1 = 0,x2 = 1,y1 = 1,x,y,temp_phi = phi, temp1, temp2;
    while (e > 0){
        temp1 = temp_phi/e;
        temp2 = temp_phi - temp1 * e;
        temp_phi = e;
        e = temp2;

        x = x2- temp1* x1;
        y = d - temp1 * y1;

        x2 = x1;
        x1 = x;
        d = y1;
        y1 = y;
        if (temp_phi == 1) return d + phi;
    }
    return -1;
}

void KeyChain::print(){
    cout<<"Your private key:\t";
    priv.print();
    cout<<"Your public key:\t";
    pub.print();
    cout<<std::endl;
    return;
}

