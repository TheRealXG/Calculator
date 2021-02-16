# Use GDB to Manipulate Program Memory
**Write a simple program that takes an input and stores it as an int and
a way to recall it. And print out the memory location of that int.**

> int stored;
> 
> while(true)
> 
> {
> 
> printf("Address of stored: %p\\n", &stored);
> 
> int input;
> 
> printf("Type a single integer; 9=recall;0=exit\\n");
> 
> scanf("%d", &input);
> 
> if(input == 9)
> 
> {
> 
> printf("Stored Number is: %d\\n", stored);
> 
> } else if(input ==0)
> 
> {
> 
> exit (0);
> 
> } else
> 
> {
> 
> stored = input;
> 
> }
> 
> }

**Start QEMU as you normally would, but adding the -s command.**

`-s` Shorthand for -gdb tcp::1234, i.e. open a gdbserver on TCP port 1234\.

**Run arm-rtems-gdb from the tools folder compiled for arm-rtems**

**Once running, connect to the gdb server running on qemu:**

`(gdb) target remote :1234`

**You should know the memory location of the int stored from the output.
Examine the memory by using the x command in gdb**

`(gdb) x/1dw 0x2080b0`  

Returns:  
`0x2080b0: 1`

**Set that memory to a different integer with the following command**

`(gdb) set \*((int \*) 0x2080b0) = 2`

**Use the continue command in gdb to return execution to the
executable**

`(gdb) continue`

**Use your recall button to ensure that int stored was changed**
