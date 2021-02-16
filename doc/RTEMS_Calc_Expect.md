# Modify Caluclator Application to Automate with Expect
This tutorial modified the Calculator application to accept user input
and create an Expect script to automatically run the Calculator App in
QEMU and provide user input and asses the validity of the output based
on a passed expected output value.

This tutorial assumes you have already done the [basic calculator RTEMS
setup](RTEMS_QEMU_Calc_Walkthrough.md)

Install Expect:\
`sudo apt install expect`

This assumes the RTEMS Quick start and Calculator was performed and you
are now working in:

`\~/quick-start/calc4waf`

First, modify the man/main.c file to accept user input. This can be see
in the Azure Git Repo "Calculator" (not very accessible) in the
Expect\_Script branch. Using Git is preferable, but for reference the
code can be found at this
[link](https://dodtelework.sharepoint.com/:u:/s/TheRealXG/Eb_cZ35KAMVDmUmxZLKnCqQBMmOIe--C_ffbBPd94R4Bwg?e=6BArUz)
which should be downloaded and placed in calc4waf\\man to replace
main.c.

Next, re-build the application in \~/quick-start/calc4waf

> ./waf configure \--rtems=\$HOME/quick-start/rtems/5
> \--rtems-bsp=arm/realview\_pbx\_a9\_qemu
>
> ./waf

Next, create a text file called "Test\_Calculator.exp" in
/*quick-start/calc4waf/build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems*

In this file, place:

> \#!/usr/bin/expect -f
>
> \# Wait enough (forever) until a long-time boot
>
> set timeout --1
>
> set val\_1 \[lindex \$argv 0\]
>
> set val\_2 \[lindex \$argv 1\]
>
> set output \[lindex \$argv 2\]
>
> set failMsg \"\\n\\nTest Fail: \\n\\r\"
>
> set passMsg \"\\n\\nTest Pass: \\n\\r\"
>
> \# Start the guest VM
>
> spawn qemu-system-arm -net none -no-reboot -nographic -monitor none
> -serial stdio -M realview-pbx-a9 -m 256M -kernel calc.exe
>
> \# Save output to this log file
>
> log\_file -noappend test\_calculator.log
>
> \# Wait for the prompt to enter values to sum
>
> expect \"Enter 1st Value\*\"
>
> send \$val\_1\\n
>
> expect {
>
> \"Enter 2nd Value\*\" {send \$val\_2\\n}
>
> \"Invalid Number\" {puts \$failMsg; exit}
>
> }
>
> expect {
>
> \"Final Output: \$output\" { puts \$passMsg }
>
> \"Final Output: ?\" { puts \$failMsg }
>
> \"Invalid Number\" { puts \$failMsg }
>
> }
>
> interact

Then run:\
\
`chmod +x example.exp`

Finally, run the Expect script with:

> ./Test\_Calculator.exp 1 2 3

This will run the Expect script and output to the screen and the log
file. It will add 1 and 2 and expect to see 3. It will output "Test
Pass:" to the screen and the application terminal output will be saved
to the test\_calculator.log log file. It will not save the "Test Pass:"
text to the log file.

If you run other examples such as:

> ./Test\_Calculator.exp 1 2 4
>
> ./Test\_Calculator.exp 1 44 45

It will output "Test Fail:" since 1+2 does not equal 4. In the second
case, the Calculator can only accept single digit integer inputs so "44"
will cause an invalid input which will produce a fail.

To see output that includes the Pass/Fail output, run it like this:

> ./Test\_Calculator.exp 1 2 3 \|tee test\_console.log
