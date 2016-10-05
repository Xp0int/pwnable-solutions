#ifndef KEY_H
#define KEY_H

#include <iostream>

using std::cout;

class Key{
    private:
        unsigned a;
        unsigned b;
    public:
        void setfirst( unsigned f){a=f; return;};
        void setsecond( unsigned s){b=s; return;};
        void setlast( unsigned s){b=s; return;};
        Key(unsigned ar, unsigned br){a=ar; b=br;};
        Key(){};
        unsigned getfirst(){return a;};
        unsigned getsecond(){return b;};
        unsigned getlast(){return b;};
        void print(){cout<<"("<<a<<","<<b<<")"<<std::endl; return;}
};

class KeyChain{
    private:
        Key priv;
        Key pub;
        void generate_keypair(const  unsigned &p, const  unsigned &q);
        unsigned multiplicative_inverse( unsigned e,  unsigned phi);
        bool ready;
    public:
        KeyChain();
        KeyChain( unsigned p,  unsigned q){generate_keypair(p,q);};
        Key* getpub(){return &pub;};
        Key* getpriv(){return &priv;}; 
        void print();
        bool isready(){return ready;};
};



#endif
