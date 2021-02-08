# Introduction 
This code is a simple Calculator example generated from an ANSYS Model Based Engineering model. The tool auto-generated this code, which then had the build file modified to allow building this with RTEMS.

# Getting Started
See source [Teams Document](https://dodtelework.sharepoint.com/:w:/r/sites/TheRealXG/_layouts/15/Doc.aspx?sourcedoc=%7B532D209A-A593-4293-B97F-2C0D48470E42%7D&file=RTEMS_QEMU_Calc_Walkthrough.docx&action=default&mobileredirect=true).
This example is how to build a simple Calculator Example (source provided) and run it in RTEMS 5 within QEMU. This uses the Realview-PBX-A9 BSP which is an ARM architecture that RTEMS specifically notes is suitable for QEMU. This assumes an Ubuntu installation. This attempts to provide instructions for all necessary dependencies, though it is not guaranteed considering how many things have been installed prior to this example. 

This uses the [RTEMS Quick Start guide](https://docs.rtems.org/branches/master/user/start/index.html#) as a basis:
1. First install QEMU, this can be done from the terminal with:  
	`sudo apt-get install qemu-system`
2. Then install the following dependencies (these may not all be necessary, but they are ones I installed over time from tutorials such as [this](http://alanstechnotes.blogspot.com/2013/03/setting-up-rtems-development.html) and the first several are likely already installed with your Ubuntu)  
	    `sudo apt-get install build-essential`  
	    `sudo apt-get install git`  
	    `sudo apt-get install python-dev`  
	    `sudo apt-get install pax`  
	    `sudo apt-get build-dep binutils gcc g++ gdb unzip git python2.7-dev pax` 
	1. To use “build-dep” in Ubuntu for the first time you need to add source repositories to the install list.  
	2. Open “Software & Updates” and check “Source code”  
	3. Then Close and in the terminal run  
		`sudo apt update`
	4. And then try the build-dep command above again  
3. This example uses the released builds of RTEMs rather than the Git repo, see 2.3.1 in RTEMS documentation. Theses acquire the released builds of the RTEMS Source Builder tool and the RTEMS Kernel Source  
		`mkdir -p $HOME/quick-start/src`  
		`cd $HOME/quick-start/src`  
		`curl https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-source-builder-5.1.tar.xz | tar xJf -`  
		`cd $HOME/quick-start/src`  
		`mv rtems-source-builder-5.1 rsb`  
		`cd $HOME/quick-start/src`  
		`curl https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-5.1.tar.xz | tar xJf -`  
4. Next is to build/install the toolchain following section 2.4.  
		`cd $HOME/quick-start/src/rsb/rtems`  
		`../source-builder/sb-set-builder --prefix=$HOME/quick-start/rtems/5 5/rtems-arm`  
	1. This may take awhile to run (10min-3hr depending on your machine and if you’ve run source builder before)  
	2. Check your install and version with  
	`$HOME/quick-start/rtems/5/bin/arm-rtems5-gcc –version`  
5. Next is to Build and Install a BSP (Realview-PBX-A9), per section 2.5.1  
		`../source-builder/sb-set-builder --prefix=$HOME/quick-start/rtems/5 \ 
--target=arm-rtems5 --with-rtems-bsp=realview_pbx_a9_qemu --with-rtems-tests=yes 5/rtems-kernel`  




# Build and Run
1.	In the Git Repo main directory ($GIT_REPO), execute the following:  
	`./waf configure --rtems=$HOME/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu`  
2.	Then compile with:  
	`./waf`
3.	The compile application has now been placed in  
	`$GIT_REPO/build/arm-rtems5-realview_pbx_a9_qemu/rtems`
4.	To run the application using QEMU:  
	`export QEMU_AUDIO_DRV="none"`  

	`qemu-system-arm -net none -no-reboot -nographic -M realview-pbx-a9 -m 256M -kernel $GIT_REPO/build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe`

# Test
1. This branch is setup to use the Robot Test Framework for testing which first needs installed  
	(Assuming Python 3 is already installed)  
	`pip3 install robotframework`  
	`pip3 install docutils`  
2. In the main Calculator folder execute  
	`robot testScripts/keyword_driven.robot`  
	This will run 7 basic test cases (4P/3F) and report the results to the command line. Test details can be viewed by opening `log.html`  
3. To execute all Robot tests in the folder run  
	`robot testScripts/.`  
4. For Data Driven tests, first run  
	`pip3 install --upgrade robotframework-datadriver`  
	`robot testScripts/data_driver.robot`  
	This will execute a test that reads in a CSV of expressions to test `data_driver.csv`  
	Expressions can be entered on a new line with the first entry being the input expression then the expected output.  
5. To generate XUnit XML output in results.xml, run  
	`robot --xunit results testScripts/.`
6. More tests and development is in work on this testing framework

# Contribute
TODO: Explain how other users and developers can contribute to make your code better.  
To generate Robot Custom Library documentation:  
	`python3 -m robot.libdoc testScripts/CalculatorLibrary.py Calc_Lib.html`  
To generate HTML documentation on Test Cases:  
	`python3 -m robot.testdoc testScripts/*.robot test_Doc.html`

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)