CC=cc
CFLAGS=-O3
pwn : pwn.o gadget.o base64.o md5.o login.o tuple.o
	$(CC) $(CFLAGS) -o pwn pwn.o gadget.o base64.o md5.o login.o tuple.o

pwn.o : pwn.c
	$(CC) $(CFLAGS) -c pwn.c

gadget.o : gadget.c
	$(CC) $(CFLAGS) -c gadget.c

base64.o : base64.c
	$(CC) $(CFLAGS) -c base64.c

md5.o : md5.c
	$(CC) $(CFLAGS) -c md5.c

login.o : login.c
	$(CC) $(CFLAGS) -c login.c

tuple.o : tuple.c
	$(CC) $(CFLAGS) -c tuple.c

clean:
	rm pwn.o gadget.o md5.o base64.o login.o tuple.o
