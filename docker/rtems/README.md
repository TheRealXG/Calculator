# Introduction 
This is the dockerfile that is used to create the docker image for building RTEMS ARM BSPs and applications from the command line without install any RTEMS dependencies, etc.

# Getting Started
Download and install Docker on a development computer - [Get Docker](https://docs.docker.com/get-docker/).

# Build and Run
1.	In the same directory as the Dockerfile, execute the following:  
	`docker build -t rtems-arm-6 .`  
	(The image is also available already built on DockerHub as `therealxg/azure_pipeline:rtems_6_build`, swap this in for `rtems-arm-6` below and ensure you are logged into DockerHub with access to this private repository.)
2.	To configure the RTEMS application build, create a `config.ini` file in the top level source code directory that specifies your desired BSP and any BSP build options. It should generally contain the following options, and more can be appended:  
```
[arm/xilinx_zynq_a9_qemu]
BUILD_TESTS = False
BUILD_SAMPLES = False
```  
3. To run the container, either navigate to the top level source code directory containing the `wscript` file, or change `"$(pwd)"` to be that top level directory. Then launch the container with:  
	`docker run -it --rm -v "$(pwd)":/src rtems-arm-6`  
	
  
# More Information
Docker run flags used: 

    -t, --tty                            Allocate a pseudo-TTY
    -i, --interactive                    Keep STDIN open even if not attached
    --rm                                 Automatically remove the container when it exits
    -v, --volume list                    Bind mount a volume
    -e,                                  Pass in an environment variable
  

# Alternative Run Methods
## Execute a Clean and Build
`docker run -it --rm -v "$(pwd)":/src rtems-arm-6 ./waf clean build`  

## Build with the LIBBSD networking library
First, ensure the config.ini file includes the following lines:
```
RTEMS_NETWORKING = False
RTEMS_POSIX_API = True
```
Then, run the following Docker command to include the LIBBSD networking library.  
`docker run -it --rm -e LIBBSD=y -v "$(pwd)":/src rtems-arm-6`  

## Copy out the RTEMS build libraries
If you wish to copy out the RTEMS build libraries from the container for use in other applications, such as a static analysis tool, the following command can be executed to copy the `rtems/6` folder into the current directory.  
`docker run -it --rm -v "$(pwd)":/src rtems-arm-6 cp -r /development/rtems/ .`


 

# Contribute
If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
