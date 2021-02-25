#!/bin/bash

#set QEMU_AUDIO_DRV to none to get rid of nag 
export QEMU_AUDIO_DRV="none"

#change to mounted git repository directory
cd /volume

#configure waf to build exe with correct rtems dir and BSP / then build
./waf configure --rtems=/rtems/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu
build-wrapper-linux-x86/build-wrapper-linux-x86-64 --out-dir $(Build.SourcesDirectory)/sonarcloud ./waf


#Run the Robot test framework on all *.robot files in testScripts. Output in main Calculator folder.
robot --xunit results testScripts/.

#debug statements
echo "Startup.sh script was ran." >> /volume/log.txt
