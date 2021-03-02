# Introduction 
This is the dockerfile that is used to create the docker image that is used to run CPPCheck on source code in the pipeline.

# Getting Started
Download and install Docker on a development computer - [Get Docker](https://docs.docker.com/get-docker/).

# Build and Run
1.	In the same directory as the Dockerfile, execute the following:  
	`docker build -t cppcheck .`  
2.	Then launch the container with:  
	`docker run --rm -v PATH_TO_SOURCECODE:/volume cppcheck`  
  
# More Information
Docker run flags used: 

    --rm                                 Automatically remove the container when it exits
    -v, --volume list                    Bind mount a volume
  

PATH\_TO\_SOURCECODE is the local folder on the host, which is attached to the container as /volume.  In these examples, the host folder contains the sorce code downloaded from this git repo.

In the pipeline, there is a CMD line at the end of the Dockerfile that will execute a bash script to control operations in the container.
Currently this start.sh script calls another script, run\_cppcheck.sh which is kept in source control, so it can be customized to fit needs. This is intended to run cppcheck against source code and output the results to /volume.  
This is the command to start the container in the pipeline:  

  `docker run -v $(Build.SourcesDirectory):/volume cppcheck`

# Contribute
If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
