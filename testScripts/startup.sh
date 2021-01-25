#!/bin/bash

#set QEMU_AUDIO_DRV to none to get rid of nag 
export QEMU_AUDIO_DRV="none"

#change to mounted git repository directory
cd /volume

#configure waf to build exe with correct rtems dir and BSP / then build
./waf configure --rtems=/rtems/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu
./waf

#Make expect script executable then run it with some default settings as of now
chmod +x /volume/testScripts/Test_Calculator.exp
/volume/testScripts/Test_Calculator.exp 1 + 5 6

#debug statements
echo "Startup.sh script was ran." >> /volume/log.txt
