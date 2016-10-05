CC=cc
CFLAGS=-O3
pwn500 : pwn500.o package.o receiver.o sender.o gadget.o list.o
	$(CC) $(CFLAGS) -o pwn500 pwn500.o package.o receiver.o sender.o gadget.o list.o

pwn500.o : pwn500.c
	$(CC) $(CFLAGS) -c pwn500.c

package.o : package.c 
	$(CC) $(CFLAGS) -c package.c

receiver.o : receiver.c 
	$(CC) $(CFLAGS) -c receiver.c

sender.o : sender.c 
	$(CC) $(CFLAGS) -c sender.c

gadget.o : gadget.c
	$(CC) $(CFLAGS) -c gadget.c

list.o : list.c
	$(CC) $(CFLAGS) -c list.c

clean:
	rm pwn500.o receiver.o sender.o package.o gadget.o list.o
