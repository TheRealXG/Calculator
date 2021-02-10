# Introduction 
This code is a simple Calculator example generated from an ANSYS Model Based Engineering model. The tool auto-generated this code, which then had the build file modified to allow building this for Windriver Linux.

# Getting Started
This example is how to build a simple Calculator Example (source provided) and run it in Windriver Linux within QEMU. This uses the qemuppc BSP which is a PowerPC architecture that Windriver specifically notes is suitable for QEMU. This assumes an Ubuntu installation. This attempts to provide instructions for all necessary dependencies, though it is not guaranteed considering how many things have been installed prior to this example. 

This uses the [Wind_River_Linux_Platform_Development_Quick_Start_LTS_19](https://docs.windriver.com/bundle/Start_here_Wind_River_Linux_Platform_Development_Quick_Start_LTS_19/) as a basis:

1. Install the following dependencies per [Necessary Linux Host System Libraries and Executables](https://docs.windriver.com/bundle/Wind_River_Linux_Release_Notes_LTS_19/page/mmo1403548614704.html):
   ```
   sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib \
   build-essential chrpath socat cpio python python3 python3-pip python3-pexpect \
   xz-utils debianutils iputils-ping libsdl1.2-dev xterm
   ```

2. Set up the platform development environment by following these steps from [Setting Up the Platform Project Development Environment](https://docs.windriver.com/bundle/Start_here_Wind_River_Linux_Platform_Development_Quick_Start_LTS_19/page/yqh1605740795305.html):
   1. Create a directory for your platform project and navigate to it  
      `mkdir -p wrl`  
      `cd wrl`  
   2. Clone the Wind River Linux Git repository   
      `git clone --branch WRLINUX_10_19_BASE https://github.com/WindRiver-Labs/wrlinux-x`
   3. Run **setup.sh** to define your project configuration  
      `./wrlinux-x/setup.sh --machines qemuxppc`  
   4. Set up the development environment. This step must be performed each time you work on your project  
      `. ./environment-setup-x86_64-wrlinuxsdk-linux`  
      `. ./oe-init-build-env`  

3. Customize the platform project by following these steps from [Customizing the Platform Project](https://docs.windriver.com/bundle/Start_here_Wind_River_Linux_Platform_Development_Quick_Start_LTS_19/page/gqv1605740798121.html):  
   1. Open the projectDir/build/conf/local.conf in an editor
      - This is wrl/build/conf/local.conf
   2. Edit the BB_NO_NETWORK option to enable network access.
      - Set the BB_NO_NETWORK option to 0 (zero).  
        `BB_NO_NETWORK ?= "0"`  
   3. Add a template to add the gdb and gdbserver development packages.
      - Edit the WRTEMPLATE option to include the feature/gdb template.  
        `WRTEMPLATE ?= "feature/gdb"`
   4. Build the platform project image.  
      `bitbake wrlinux-image-small`  
4. Deploy the platform project by following these steps from [Deploying the Platform Project Image](https://docs.windriver.com/bundle/Start_here_Wind_River_Linux_Platform_Development_Quick_Start_LTS_19/page/snd1605740797216.html):  
   1. Deploy the platform project  
      `runqemu qemuppc`  

# Generating the SDK
Generate the software development kit by following the steps from [Generating the SDK](https://docs.windriver.com/bundle/Wind_River_Linux_Platform_Developers_Guide_9_1/page/faq1518556223077.html):  
   1. Set up the development environment.  
      `. ./environment-setup-x86_64-wrlinuxsdk-linux`  
      `. ./oe-init-build-env build`  
      
   2. Update the build directory conf/local.conf file to set the SDK variable.
      - Open the projectDir/build/conf/local.conf in an editor  
        This is wrl/build/conf/local.conf  
	Add the folowing line:  
        `SDKMACHINE = "x86_64"`  
	
   3. Generate the SDK.  
      `bitbake -c  populate_sdk wrlinux-image-small`  
   
   4. Install the SDK on the host.  
      `./tmp-glibc/deploy/sdk/wrlinux-10.19.45.15-glibc-x86_64-qemuppc-wrlinux-image-small-sdk.sh`  
      
# Adding a package to the platform build
1. Create a directory for your platform project and navigate to it  
   `mkdir -p ~/wrl/layers/local/recipes-sample/calc`  
   `cd ~/wrl/layers/local/recipes-sample/calc`  
2. Clone the calculator Git repository   
   `git clone --branch wrl https://github.com/TheRealXG/Calculator.git`  
3. Add your package to the platform project build.  
   - Open the build directory conf/local.conf file in an editor and add the following line:  
     `IMAGE_INSTALL_append +=  " calc"`  

4. Build the file system to include the package in your platform project image.  
   `bitbake wrlinux-image-small`  
   
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
