all: hellomake

hellomake: hello_world.c
	gcc hello_world.c -o program  
	
clean:
	-rm -f program
