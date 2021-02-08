INCLUDE=-Igen -Iman 

all:
	$(CC) $(CFLAGS) gen/*.c man/*.c $(INCLUDE) -o calc

clean:
	rm -f calc

run: calc
	./calc

