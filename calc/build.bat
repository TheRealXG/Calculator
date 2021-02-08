set GCC=C:\Program Files\ANSYS Inc\v202\SCADE\contrib\Msys64\mingw64\bin\gcc.exe

del calc.exe 2>nul
"%GCC%" gen/*.c man/*.c -Igen -Iman -o calc.exe

pause
