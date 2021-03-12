#!/bin/bash

if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

cd $SRC_VOL

#set QEMU_AUDIO_DRV to none to get rid of nag
export QEMU_AUDIO_DRV="none"

#Run the Robot test framework on all *.robot files in testScripts. Output in main Calculator folder.
robot --xunit results testScripts/.

echo "start_test.sh scrip was run." >> $SRC_VOL/log.txt
