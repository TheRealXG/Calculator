# Setup RTEMS Calculator Code and QEMU Debugging in Eclipse
  
0. Assumes you have RTEMS already built for Realview PBX A9 board per [previous tutorials]( https://teams.microsoft.com/l/file/532D209A-A593-4293-B97F-2C0D48470E42?tenantId=21acfbb3-32be-4715-9025-1e2f015cbbe9&fileType=docx&objectUrl=https%3A%2F%2Fdodtelework.sharepoint.com%2Fsites%2FTheRealXG%2FShared%20Documents%2FQEMU%2FRTEMS_QEMU_Calc_Walkthrough.docx&baseUrl=https%3A%2F%2Fdodtelework.sharepoint.com%2Fsites%2FTheRealXG&serviceName=teams&threadId=19:19b3ba71269b4d189d902dc25e24a170@thread.skype&groupId=8a0bcbd8-2310-4c1d-8099-fe9701f3f461).  
1. Install Eclipse (2020-12 was used), [download link for Linux](https://eclipse.bluemix.net/packages/2020-12/data/eclipse-inst-jre-linux64.tar.gz).  
2. Git clone the Calculator project and checkout the Eclipse branch (or master once merged)  
3. Launch Eclipse, accept default Workspace  
4. File->Open projects from file system  
	+ Click Directory... and choose your Calculator folder  
	+ Click Finish. This will open the project, it will have to do some C indexing at import  
		(Do any paths need updated in project preferences?)  
	+ Close the welcome screen.  
5. Create WAF Builder  
	+ Right-click Calculator Project and seelct Properties  
	+ Choose Builders->New...->Program->OK  
	+ Name it `WAF`
	+ Location: Browse Workspace, select Calculator->WAF  
	+ Working Directory: Browse Workspace, select Calculator top level folder->OK  
	+ In arguments enter `configure --rtems=/home/jimbrewer/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu build` but UPDATE with your appropriate paths and click OK  
	+ Under Builders it may have "Invalid External Tool Builder" listed which should be Removed  
	+  Apply and Close  
6. Import Debug Config  
	+ Select File->Import  
	+ Select Run/Debug->Launch Configurations->Next  
	+ Browse to the Calculator folder and select Open  
	+ Select the checkbox next to the Calculator Folder and ensure `Calculator_GDB + Remote.launch` now has a check box  
	+ Click Finish  
7. Check paths and settings  
	+ Check Project Includes  
		- Right-click the project and select Properties  
		- Navigate to C/C++ General->Paths and Symbols->Includes->GNU C  
		- Edit the include path to map to your RTEMS `$PREFIX/arm-rtems5/realview_pbx_a9_qemu/lib/include`  
		- Apply and Close  
	+ Run->Debug Configurations->C/C++ Remote Application->Calculator_GDB Remote  
		- Update the path under Main->C/C++ Application: to where you Calculator folder is located.  
8. Build Program  
	+ With Calculator selected, choose Project->Build Project  
	+ The first time it is built after a Clone the build may fail. Build again and it should succeed  
	+ To verify build, navigate to `Calculator/build/arm-rtems5-realview_pbx_a9_qemu/rtems` which should contain `calc.exe`  
9. Run Program  
	+ Right-click the project Calculator->Show in Local Terminal->Terminal  
	+ This should open a terminal in Eclipse in the Calculator folder  
	+ Enter `qemu-system-arm -net none -no-reboot -nographic -M realview-pbx-a9 -m 256M -kernel build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe` and press `Enter`  
		- This will run the Calcualtor application in the terminal and can be interacted with.  
10. Debug Program  
	+ In the terminal ener `qemu-system-arm -net none -no-reboot -nographic -M realview-pbx-a9 -m 256M -kernel build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe -s` and press `Enter`  
	+ Select the drop-down arrow next to the "bug" in the toolbar and choose `Calculator_GDB Remote`  
	+ This will launch the debugger and switch Perspectives (click Switch when asked, you may want to choose the checkbox as well)  
	+ It is recommended to select Winddow->Show View->Terminal to see the Calculator interface and drag the terminal to the lower-left corner or other visible location.  
	+ You can now debug and interact with the Calculator in the Debug mode. When done debugging, you can exit the Calculator with `q` or click the red `Stop` button at the top and then click the `C/C++` Perspective button in the top-right corner of the window to return to the main editor window. See below for a Debugger tutorial.  
11. Debugger Tutorial  
	+ With the Calculator and Debugger running, ensure man/main.c is visible (Click Project Explorer in the upper-left corner and expand to find the file and open it if necessary)  
	+ Create a Breakpoint by double-clicking to the left of line 89 `root_Calc(&inC, &outC);`  
	+ Enter the number `2` into the Calculator terminal window and press `Enter`  
	+ This will pause after reading the input but before calculating a result.  
		- On the right-side of the screen is a listing of the "Variables" in the current scope, the value of `input` can be seen as a char of value `50'2'`
		- There is also a tab for "Breakpoints" that shows all current breakpoints and they can be (de)activated or removed
		- At the bottom there should be a tab called `Memory` (if not, select Window->Show View->Memory)  
		- Click the green `+` next to Monitors and type `&input` and click OK. This will show the memory allocated to this variable. You will likely see something like `7B991132` where the last 2 characters "32" is the HEx value for the ASCII character "2" you entered.  
			* You can click `+ New Renderings...` to choose a different view such as ASCII which will display a "2" in the memory at this location.  
		- Again click the green "+" next to Monitors and type `&inC.keyEvent`. This will show the memory value for the Calculator key that was set at line 40 and is being passed to the calculation function. This should show `0x02000000` or a new rendering as "Unsigned Integer" will show a "2" for the 2 that was entered to the Calculator.  
			* Right-Click the "2" in memory and select "Find and Replace". Enter Find: `02`, Replace With: `03`, Format `Hexadecimal`, Start address: `0x00204498` (or whatever your address is for inC.keyEvent) and End Address 4 Bytes later, e.g. `0x0020449B` then click `Replace`. In the Memory view the `2` should change to `3`. This changed the input value the calculator will use.  
		- Now click the Green Arrow at the top of the window to continue operations.  
		- Examine the Calculator terminal output and it should say `Display Output: 3`, rather than `2` showing you successfully manipulated memory while debugging.  
		- You can continue interacting with the Calculator in the terminal and watch the memory values change as you input values.  
			* Click the Green Arrow after each value entered,to continue operation.  
	+ Enter `q` to quit the Calculator. Then click the `C/C++` Perspective button in the upper-right corner to return to normal editing mode.  
		- You may wish to save your debugging Perspective with the Terminal and Memory windows, other other customizations, for future QEMU debugging. To do this, while in that desired view, select Window->Perspective->Save Perspective As... and give it a name or overwrite the current Debug Perspective.  
		- To set a new perspective as the default when debugging, indow->Preferences->Run/Debug->Perspectives  
			* Select C/C++ Remote Application->GDB (DSF) Manual Remote  
			* Choose your new Perspective,  and click `Apply and Close`




### Setup with a new project in Eclipse  
This is not needed for the Calculator project since it already has an Eclipse `.project` file. These were the steps needed to set that up and could be used for a enw RTEMS project.  
1. Assuming the project is already cloned to your computer.  
2. File->Import  
3. Select Git->Projects from Git->Next  
	- Existing local repository->Next  
	- Choose Repo->Next  
4. Import using the New Project wizard->Finish  
	- Makefile Project with Existing Code->Next  
	- Uncheck C++  
	- Enter name (Calculator)  
	- Choose Existing Code Location (your already cloned git repo)  
	- <none> tool chain->Finish  
5. Right-click the project and select Properties.  
	- Under C/C++ General->Paths and Symbols->Includes->GNU C->Add...->File System...  
		* Chooses your RTEMS PREFIX location and BSP include folder, e.g. `/home/jimbrewer/quick-start/rtems/5/arm-rtems5/realview_pbx_a9_qemu/lib/include`  
		* Apply and Close  
		* Rebuild Index when it asks (or right-click project->Index->Rebuild) to remove warnings for  unresolved types.  
6. If you have yellow "unresolved includes" for standard C libraries then:  
	- Right-click the project and select Properties.  
		* Under C/C++ General > Preprocessor Includes > Providers and select both:  
			- "CDT GCC Built-in Compiler Settings"
			- "CDT CROSS GCC Built-in Compiler Settings" then select "Use global provider shared between projects"  
		* Apply and Close
