# Setup Eclipse and SonarLint

This will setup the SonarLint plug-in in Eclipse. This will show possible "Code Smells", "Vulnerabilities", and other code issues while coding.

This can be "bound" to the Sonarcloud online project in order to:  
* Settings set on server side - quality profiles, custom analysis settings, quality gates - are shared with all members of your team  
* Issues suppressed as “won’t fix” or “false positive” on the server won’t show up in SonarLint  
* Some languages are only available in connected mode (Such as C)  
* Optional notifications keep you informed of your project’s quality gate status  

1. Open Eclipse with the Calculator Project already setup.  
2. Help->Eclipse Marketplace...  
3. Search `sonarlint`  
4. Click Install and Accept license agreement  

[Connect to Sonarcloud](https://github.com/SonarSource/sonarlint-eclipse/wiki/Connected-Mode)   
In Eclipse:  
1. File->New->Other  
2. SonarLint->New SonarQube/SonarCloud Connection  
3. Select sonarcloud  
4. Enter User Token from Sonarcloud (Generate it on Sonarcloud from My Account->Security->Tokens)  
Click Next several times and then Finish  
5. Select Projects to Bind.
6. Click "Add" and choose Calculator (double click)
7. Click Next, ensure it matches with the correct Sonarcloud Project, then Finish  
Under the SonarLint Bindings view, you can right-click on SonarCloud and select `Update All Project Bindings` to update settings from the server (such as which files to include in analysis).  


See issues highlighted in source code with light blue or red "squiggly". Click on that text and see the context menu showing the issue. You can click on options to see the issue elsewhere and to see a rule description to show the preferred method of implementation.


Under Window->Show View->Other->SonarLint you can see other view options that will show in the Perspective.  

* SonarLint Report  
	Right-click the project in the side-bar and select SonarLint->Analzye, or Analyze Changed Files. BThis will produce a report of findings. It seems this will sometimes find more items than seen on the server. This will show findings from local analysis, it is not showing server analysis. For some reason it has some issues thinking files are CPP rather than C files. Attempted to fix by ensuring the "Project Nature" in Eclipse didn't include C++. Also in Project Settings under C/C++ General->File Types changed to use Project Settings and explicitly specify that \*.c is a C source file and \*.h is a C header file. This worked for other people, but didn't seem to help this issue. Was able to change the Quality Profile on Sonarcloud to disable C++ rules and the issue went away after updating the binding, though this is a bit of a work around. There were still a few extra findings for some unknown reason. After this there were only 2 remaining additional findings locally than remotely.  
	
	Occasionally a warning comes up saying some rules cannot be analyzed, but it does not give more detail on how to fix this.  
	 
	Theoretically with Remote Binding it will not show "Won't Fix" issues if it works.  


* SonarLint On The Fly  
	This will show issues on recently edited or opened files. You can double click the issue to go to it. Right-click the issue for the Rule Description. This will be the most useful window while actively developing.  