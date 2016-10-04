#Makefile for RSA

CXX=g++
CFLAGS=-Wall

EXE=RSA.out
SRCDIR=src
INCLUDE=-I$(SRCDIR) -I.
LIB=
SRCS=rsamath.cpp key.cpp rsaCipher.cpp
OBJ=$(SRCS:%.cpp=%.o) main.o

all: $(EXE)

$(EXE): $(OBJ)
	$(CXX) $(LIB) $^ -o $@

%.o: $(SRCDIR)/%.cpp $(SRCDIR)/%.h
	$(CXX) $(LIB) $(INCLUDE) $(CFLAGS) -c $<

.cpp.o:
	$(CXX) $(LIB) $(INCLUDE) $(CFLAGS) -c $<

.PHONY: clean
clean:
	rm -rf $(OBJ) *~ $(SRCDIR)/*~
