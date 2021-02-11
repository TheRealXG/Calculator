# Introduction 
This is the dockerfile that is used to create the docker image that is used in the Windriver Linux pipeline.

# Getting Started
Download and install Docker on a development computer - [Get Docker](https://docs.docker.com/get-docker/).

# Build and Run
1.	In the same directory as the Dockerfile, execute the following:  
	`docker build -t wrl .`  
2.	Then launch the container with:  
	`docker run -ti --rm -v D:\docker\WRL\volume:/volume wrl /bin/bash`
  
# More Information
Docker run flags used: 

    -t, --tty                            Allocate a pseudo-TTY
    -i, --interactive                    Keep STDIN open even if not attached
    --rm                                 Automatically remove the container when it exits
    -v, --volume list                    Bind mount a volume
  

/bin/bash is used on the end of the run command to start an interactive bash session

In the pipeline, there is a CMD line at the end of the Dockerfile that will execute a bash script to control operations in the container.
Currently this start.sh script calls another script, startup.sh which is kept in source control, so it can be customized to fit needs.
This is the command to start the container in the pipeline:

  `docker run -v $(Build.SourcesDirectory):/volume wrl`

# Contribute
If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
