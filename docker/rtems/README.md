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

## Use in Gitlab CI Pipeline
If you wish to use this in a Gitlab CI Pipeline defined by YAML, you can use this as the job container image (Docker or Kubernetes executor) but the ENTRYPOINT will not be executed, so the entrypoint script will need explicitly called. Additionally, 1-2 variables will need set to provide correct directories to the script. To call the image and have a blank entrypoin, for the applicable job add:
```
image:
    name: registry.gitlab.com/therealxg/calculator/modular_pipeline:rtems_6_build_ubi8-2
    entrypoint: [""]
```  
Then, use the script command with several additional commands. This sets the Source code Directory, the image will assume it is mapped to `/src`, as above, if nothing is specified, but Gitlab will not allow the Git repo to be checked out to that location, so the Gitlab repository checkout location is set. Then the `config_compile.sh` scripe is called explicitly, followed by the build command. The final command copies out the build executable to the top level directory for use by later testing jobs, artifact saving, etc.  
```
script:
    - echo "Run build container"
    - export SRCDIR=$CI_BUILDS_DIR/$CI_PROJECT_PATH
    - /usr/local/bin/config_compile.sh
    - ./waf clean build
    - cp build/*/rtems/*.exe .
```
If you wish to use the RTEMS build libraries in later jobs, e.g. SonarCloud requires them, you can add several more steps to the script command above.  
```
    - mkdir -p $CI_BUILDS_DIR/$CI_PROJECT_PATH/rtems
    - cp -r /development/rtems/. $CI_BUILDS_DIR/$CI_PROJECT_PATH/rtems
    - export PREFIXDIR=/builds/therealxg/Calculator/rtems
    - build-wrapper/build-wrapper-linux-x86-64 --out-dir bw-output ./waf clean build
```  
This creates a path in the top level directory that can be replicated in the Sonar Cloud image to keep absolute paths the same between the build and analyze stage. Then the internal RTEMS build libraries from the container are copied there and that set as the RTEMS configure PREFIX directory. Finally, for Sonar Cloud specifically, the `./waf clean build` command is preceded by the build wrapper (Sonar Cloud would have set this up in a previous stage).  

 

# Contribute
If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
