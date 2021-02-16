# Convert Calculator Application to compile for RTEMS with WAF
Setup the application work space. Create a new Git repository, download
the Waf build system, and the [RTEMS
Waf](https://git.rtems.org/rtems_waf.git/tree/README).

Create the application directory and change into it:

> mkdir -p \$HOME/calc
>
> cd \$HOME/calc

Extract the contents of the calculator archive to this folder.

Download the Waf build system and set it to executable:

> curl https://waf.io/waf-2.0.19 \> waf
>
> chmod +x waf

Initialise a new Git repository:

> git init

Add RTEMS Waf support as a Git sub-module and initialise it:

> git submodule add git://git.rtems.org/rtems\_waf.git rtems\_waf

Create the application source files (for the example
<https://dodtelework.sharepoint.com/sites/TheRealXG/Shared%20Documents/QEMU/ansys_calc.7z>
can be used. Extract and move the contents of the "integration" folder
in the zip file into \$HOME/calc)

Take a look at the build.bat from ANSYS to learn how to build the
calculator app, and which files are involved.

> \"%GCC%\" gen/\*.c man/\*.c -Igen -Iman -o calc.exe

This simple build line tells us to use all .c files in the gen/ and man/
folders, and Include the gen/ and man/ folders. A .c file called init.c
that will configure RTEMS is required.

Using an editor, create a file called man/init.c and copy the following
configuration settings:

> /\*
>
> \* Simple RTEMS configuration
>
> \*/
>
> \#define CONFIGURE\_APPLICATION\_NEEDS\_CLOCK\_DRIVER
>
> \#define CONFIGURE\_APPLICATION\_NEEDS\_CONSOLE\_DRIVER
>
> \#define CONFIGURE\_UNLIMITED\_OBJECTS
>
> \#define CONFIGURE\_UNIFIED\_WORK\_AREAS
>
> \#define CONFIGURE\_RTEMS\_INIT\_TASKS\_TABLE
>
> \#define CONFIGURE\_INIT
>
> \#include \<rtems/confdefs.h\>

The main function in man/main.c will need to be redefined from int
main() to this function definition for RTEMS:

> rtems\_task Init(
>
> rtems\_task\_argument ignored
>
> )

An additional include file needs to be added in the man/user\_marcros.h
file.

> \#include \<rtems.h\>

Finally create the Waf script. From the original Hello world script, the
target .exe has been changed, an "includes = 'gen man' has been added,
and the source has changed to include all .c files needed for the
calculator. Using an editor create wscript and copy the Waf script:

> \#
> 
> \# Hello world Waf script
> 
> \#
> 
> from \_\_future\_\_ import print\_function
> 
> rtems\_version = \"5\"
> 
> try:
> 
> import rtems\_waf.rtems as rtems
> 
> except:
> 
> print(\'error: no rtems\_waf git submodule\')
> 
> import sys
> 
> sys.exit(1)
> 
> def init(ctx):
> 
> rtems.init(ctx, version = rtems\_version, long\_commands = True)
> 
> def bsp\_configure(conf, arch\_bsp):
> 
> \# Add BSP specific configuration checks
> 
> pass
> 
> def options(opt):
> 
> rtems.options(opt)
> 
> def configure(conf):
> 
> rtems.configure(conf, bsp\_configure = bsp\_configure)
> 
> def build(bld):
> 
> rtems.build(bld)
> 
> bld(features = \'c cprogram\',
> 
> target = \'rtems/calc.exe\',
> 
> cflags = \'-g -O2\',
> 
> includes = \'gen man\',
> 
> source = \[\'man/main.c\',
> 
> \'man/init.c\',
> 
> \'man/memcpy.c\',
> 
> \'man/printUtils.c\',
> 
> \'gen/kcg\_types.c\',
> 
> \'gen/root\_Calc.c\',
> 
> \'gen/kcg\_consts.c\',
> 
> \'gen/key2Char\_Calc.c\',
> 
> \'gen/valueEntry\_Calc.c\',
> 
> \'gen/performFunction\_Calc.c\',
> 
> \'gen/updateDisplay\_Calc\_Utils.c\'\])
> 

Configure the application using Waf's configure command:

> ./waf configure \--rtems=\$HOME/quick-start/rtems/5
> \--rtems-bsp=arm/realview\_pbx\_a9\_qemu

Build the application:

> ./waf

Final application, calc.exe, is placed in:

\$HOME/calc/build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems
