CC=powerpc-wrs-linux-gcc 
CFLAGS=-g

all: calc
calc.o: gen/*.c man/*.c gen/*.h man/*.h

clean:
    rm -f calc calc.o
run: calc
    ./calc
