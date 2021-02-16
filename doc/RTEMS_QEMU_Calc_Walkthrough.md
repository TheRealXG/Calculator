# Calculator App in RTEMS and QEMU
This walk is how to build a simple Calculator Example (source provided)
and run it in RTEMS 5 within QEMU. This uses the [Realview-PBX-A9
BSP](https://docs.rtems.org/branches/master/user/bsps/bsps-arm.html#realview-pbx-a9)
which is an ARM architecture that RTEMS specifically notes is suitable
for QEMU. This assumes an Ubuntu installation. This attempts to provide
instructions for all necessary dependencies, though it is not guaranteed
considering how many things have been installed prior to this example.

This uses the RTEMS Quick Start guide as a basis:
<https://docs.rtems.org/branches/master/user/start/index.html>\#

1)  First install QEMU, this can be done from the terminal with:

    a.  `sudo apt-get install qemu-system`

2)  Then install the following dependencies (these may not all be
    necessary, but they are ones I installed over time from tutorials
    such as
    <http://alanstechnotes.blogspot.com/2013/03/setting-up-rtems-development.html>
    and the first several are likely already installed with your Ubuntu)

    a.  `sudo apt-get install build-essential`

    b.  `sudo apt-get install git`

    c.  `sudo apt-get install python-dev`

    d.  `sudo apt-get install pax`

    e.  `sudo apt-get build-dep binutils gcc g++ gdb unzip git
        python2.7-dev pax` (Optional)

        1.  To use "build-dep" in Ubuntu for the first time you need to
            add source repositories to the install list.

        2.  Open "Software & Updates" and check "Source code"

        3.  ![](media/image1.png){width="6.175in" height="3.0875in"}Then
            Close and in the terminal run

            a.  `sudo apt update`

        4.  And then try the build-dep command above again

3)  This example uses the released builds of RTEMs rather than the Git
    repo, see
    [2.3.1](https://docs.rtems.org/branches/master/user/start/sources.html#releases)
    in RTEMS documentation. Theses acquire the released builds of the
    RTEMS Source Builder tool and the RTEMS Kernel Source

    a.  `mkdir -p \$HOME/quick-start/src`

    b.  `cd \$HOME/quick-start/src`

    c.  `curl
        https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-source-builder-5.1.tar.xz
        \| tar xJf -`

    d.  `cd \$HOME/quick-start/src`

    e.  `mv rtems-source-builder-5.1 rsb`

    f.  `cd \$HOME/quick-start/src`

    g.  `curl
        https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-5.1.tar.xz
        \| tar xJf -`

4)  Next is to build/install the toolchain following section
    [2.4](https://docs.rtems.org/branches/master/user/start/tools.html).

    a.  `cd \$HOME/quick-start/src/rsb/rtems`

    b.  `../source-builder/sb-set-builder
        \--prefix=\$HOME/quick-start/rtems/5 5/rtems-arm`

    c.  This may take awhile to run (10min-3hr depending on your machine
        and if you've run source builder before)

    d.  Check your install and version with

    e. `\$HOME/quick-start/rtems/5/bin/arm-rtems5-gcc --version`

5)  Next is to Build and Install a BSP
    ([Realview-PBX-A9)](https://docs.rtems.org/branches/master/user/bsps/bsps-arm.html#realview-pbx-a9),
    per section
    [2.5.1](https://docs.rtems.org/branches/master/user/start/bsp-build.html#rsb-bsp-build)

    a.  `../source-builder/sb-set-builder
        --prefix=\$HOME/quick-start/rtems/5
		--target=arm-rtems5 --with-rtems-bsp=realview_pbx_a9_qemu
		--with-rtems-tests=yes 5/rtems-kernel`

6)  Download the Calculator Example source Code from
    [Teams](https://dodtelework.sharepoint.com/sites/TheRealXG/Shared Documents/QEMU/calc4waf.zip)
    and unzip the contents to:

    a.  `\$HOME/quick-start/calc4waf`

7)  Next is to build the application with the BSP using WAF. See
    [Section
    2.7](https://docs.rtems.org/branches/master/user/start/app.html) for
    a related example.

    a.  `cd \$HOME/quick-start/calc4waf`

    b.  `./waf configure \--rtems=\$HOME/quick-start/rtems/5
        \--rtems-bsp=arm/realview\_pbx\_a9\_qemu`

    c.  `./waf`

8)  calc.exe, the compiled application, has now been placed in
    \$HOME/quick-start/calc4waf/build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems

9)  To execute this with QEMU

    a.  `cd
        \$HOME/quick-start/calc4waf/build/arm-rtems5-realview\_pbx\_a9\_qemu/rtems`

    b.  `export QEMU\_AUDIO\_DRV=\"none\"`

    c.  `qemu-system-arm -net none -no-reboot -nographic -M
        realview-pbx-a9 -m 256M -kernel calc.exe`
