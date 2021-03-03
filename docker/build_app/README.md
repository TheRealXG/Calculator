# Introduction 
This is the dockerfile that is used to create the docker image for building RTEMS applications in the AZURE pipeline.

# Getting Started
Download and install Docker on a development computer - [Get Docker](https://docs.docker.com/get-docker/).

# Build and Run
1.	In the same directory as the Dockerfile, execute the following:  
	`docker build -t build_app .`  
2.	Then launch the container with:  
	`docker run -ti --rm -v SRC_CODE:/volume build_app /bin/bash`
  
# More Information
Docker run flags used: 

    -t, --tty                            Allocate a pseudo-TTY
    -i, --interactive                    Keep STDIN open even if not attached
    --rm                                 Automatically remove the container when it exits
    -v, --volume list                    Bind mount a volume
  

/bin/bash is used on the end of the run command to start an interactive bash session

SRC\_CODE is the local folder on the host, which is attached to the container as /volume.  In these examples, the host folder contains the sorce code downloaded from this git repo.

In the pipeline, there is a CMD line at the end of the Dockerfile that will execute a bash script to control operations in the container.
Currently this start.sh script calls another script, startup.sh which is kept in source control, so it can be customized to fit needs.
This is the command to start the container in the pipeline:

`docker run --user $(id -u):$(id -g) --rm -e SRC_VOL=$(Build.SourcesDirectory)/Calculator -e RTEMS_PATH=$(Build.SourcesDirectory)/RTEMS -v $(Build.SourcesDirectory)/RTEMS:$(Build.SourcesDirectory)/RTEMS -v $(Build.SourcesDirectory)/Calculator:$(Build.SourcesDirectory)/Calculator therealxg/azure_pipeline:build_app`  
  
This runs the Docker container as the agent user and passes in the source volume and RTEMS kernel and BSp as environment variables and mapped paths for access to the files and consistent paths for SonarCloud analysis.  

# Contribute
If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
