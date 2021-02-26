#!/bin/bash

#set QEMU_AUDIO_DRV to none to get rid of nag 
export QEMU_AUDIO_DRV="none"

# Create an volume to match sources directory
#mkdir -p /home/jimbrewer/myagent/_work/1/s
#cd /home/jimbrewer/myagent/_work/1/s
# Copy contents of the mounted volume to this new folder
#cp -r /volume/. .

cd $SRC_VOL

#configure waf to build exe with correct rtems dir and BSP / then build
./waf configure --rtems=/rtems/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu
build-wrapper-linux-x86/build-wrapper-linux-x86-64 --out-dir build_wrapper_output_directory ./waf clean build


#Run the Robot test framework on all *.robot files in testScripts. Output in main Calculator folder.
robot --xunit results testScripts/.

#Copy all results back to \volume before exiting Docker
#cp -fR . /volume

#debug statements
echo "Startup.sh script was ran." >> $SRC_VOL/log.txt
