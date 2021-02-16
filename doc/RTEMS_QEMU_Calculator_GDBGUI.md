# Debug using GDBGUI

https://www.gdbgui.com/installation/

`python3 -m pip install \--user pipx`

`python3 -m userpath append \~/.local/bin`

(you already have it in your PATH so in which case you wouldn't need to
restart your console. Otherwise source or restart your console to make
sure the PATh is ubdated.)

(For Ubuntu had to run this first):

`sudo apt-get install python3-venv`

Install GDBGUI

`pipx install gdbgui`

To debug the Calculator application. This assumes the Calculator app has
been built using the Quick Start instructions
[here](RTEMS_QEMU_Calc_Walkthrough.md)
(this already includes the -g debug flag).

Assumes you have GDBGUI from above install:

In \$HOME/Calculator, run

`qemu-system-arm -net none -no-reboot -nographic -monitor none -serial
stdio -M realview-pbx-a9 -m 256M -kernel
build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems/calc.exe -s`

This will start QEMU with the calculator application with a listener for
a GDB TCP connection (-s option)

In another terminal window, in \$HOME/Calculator/, run:

`gdbgui -g arm-rtems5-gdb`

This will open GDBGUI in a browser window waiting to connect. This will
also use the ARM RTEMS GBD debugger

When the GDBGUI opens, in the GDB terminal in the lower left, enter:

`file build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems/calc.exe`

This will read in the debug symbols for calc.exe

Then at the top, click the dropdown arrow and select \"Connect to
gdbserver\"

Enter in the text window next to it:

`localhost:1234`

Then click "Connect to gdbserver"

Click on \"show filesystem\" below that.

Enter the path to the main file:

`man/main.c`

And press Enter and the source code for main.c should now show.

You can select "hide filesystem" to minize the side window

You can click on a line number to insert a break point.

Now you can interact with the calculator from the terminal and click on
the \"Play\" button in GDBGUI to continue through break points. You can
also step through and into functions or select variables to see memory
values.

If you try to step into an RTEMS source code file or C library function
it will likely show assembly or an error about not finding the file.
