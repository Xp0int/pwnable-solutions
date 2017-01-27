#include "rsamath.h"
#include <iostream>
using namespace std;

bool is_prime( unsigned a){
  if(a==2) return true;
  if(a<2||a%2==0) return false;
  for( unsigned i=3;i<( unsigned)sqrt(a)+2;i+=2)
    if(a%i==0) return false;
  return true;
};


bool is_prime(int a){
	if(a==2) return true;
	if(a<2||a%2==0) return false;
	for(int i=3;i<(int)sqrt(a)+2;i+=2)
		if(a%i==0) return false;
return true;
};

bool are_coprime( unsigned a, unsigned b){
		 unsigned temp;
	while(b!=0){
		temp=a;
		a=b;
		b=temp%b;
	}
		return a==1;
};

unsigned powerwithmodule(unsigned a, unsigned exp, unsigned n){
    int bit;
    unsigned power = 1;
    while (exp) {
        bit = exp & 0x1; 
        exp >>= 1;
        if (bit == 1) {
            power = a * power % n;
        }
        a = a * a % n;
    }
    return power;
}
