# Introduction 
This code is a simple Calculator example generated from an ANSYS Model Based Engineering model. The tool auto-generated this code, which then had the build file modified to allow building this with RTEMS.

# Getting Started
See source[Teams Document](https://dodtelework.sharepoint.com/:w:/r/sites/TheRealXG/_layouts/15/Doc.aspx?sourcedoc=%7B532D209A-A593-4293-B97F-2C0D48470E42%7D&file=RTEMS_QEMU_Calc_Walkthrough.docx&action=default&mobileredirect=true).
This example is how to build a simple Calculator Example (source provided) and run it in RTEMS 5 within QEMU. This uses the Realview-PBX-A9 BSP which is an ARM architecture that RTEMS specifically notes is suitable for QEMU. This assumes an Ubuntu installation. This attempts to provide instructions for all necessary dependencies, though it is not guaranteed considering how many things have been installed prior to this example. 

This uses the [RTEMS Quick Start guide](https://docs.rtems.org/branches/master/user/start/index.html#) as a basis:
1. First install QEMU, this can be done from the terminal with: 
	a. `sudo apt-get install qemu-system`


# Build and Test
1.	In the Git Repo main directory ($GIT_REPO), execute the following:
	'./waf configure --rtems=$HOME/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu'
2.	Then compile with:
	.'/waf'
3.	The compile application has now been placed in
	'$GIT_REPO/build/arm-rtems5-realview_pbx_a9_qemu/rtems' 
4.	To run the application using QEMU:
	'export QEMU_AUDIO_DRV="none"'
	'qemu-system-arm -net none -no-reboot -nographic -M realview-pbx-a9 -m 256M -kernel $GIT_REPO/build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe'

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)