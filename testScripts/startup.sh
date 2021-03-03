#!/bin/bash

if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi
if [ -z "$RTEMS_PATH" ]; then
  export RTEMS_PATH="/rtems"
fi

#change to mounted git repository directory
cd $SRC_VOL
#configure waf to build exe with correct rtems dir and BSP / then build
./waf configure --rtems="${RTEMS_PATH}/quick-start/rtems/5" --rtems-bsp=arm/realview_pbx_a9_qemu
# Build the application with the SonarCloud wrapper around it (copied by the pipeline into the main agent working directory) 
build-wrapper-linux-x86/build-wrapper-linux-x86-64 --out-dir build_wrapper_output_directory ./waf clean build
# Copy the final binary into the top level source directory for use by later containers
cp build/arm-rtems5-realview_pbx_a9_qemu/rtems/*.exe .

#debug statements
echo "Startup.sh script was ran." >> $SRC_VOL/log.txt
