#!/bin/bash

if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

#set QEMU_AUDIO_DRV to none to get rid of nag 
export QEMU_AUDIO_DRV="none"

#change to mounted git repository directory
cd $SRC_VOL

#configure waf to build exe with correct rtems dir and BSP / then build
./waf configure --rtems=/rtems/quick-start/rtems/5 --rtems-bsp=arm/realview_pbx_a9_qemu
build-wrapper-linux-x86/build-wrapper-linux-x86-64 --out-dir build_wrapper_output_directory ./waf clean build

# Add to path and execute Sonarcloud Scan (This is downloaded in the pipeline. Should it be in Docker instead?)
# This path is dictated by the command line in the pipeline to download and extract the sonar-scanner
export PATH=$PATH:$SRC_VOL/sonar/bin
# Pass in the Git Branch name (provided by Azure) being processed for Sonarcloud to track from
if [$GIT_BRANCH = 'master']
then
	sonar-scanner -Dsonar.login=$SC_AUTH
else
	sonar-scanner -Dsonar.login=$SC_AUTH -Dsonar.branch.name=$GIT_BRANCH
fi

#Run the Robot test framework on all *.robot files in testScripts. Output in main Calculator folder.
robot --xunit results testScripts/.

# Cleanup build wrapper folder
rm -r build_wrapper_output_directory

#debug statements
echo "Startup.sh script was ran." >> $SRC_VOL/log.txt
