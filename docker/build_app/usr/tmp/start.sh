#!/bin/bash
if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

chmod +x $SRC_VOL/testScripts/startup.sh
cd $SRC_VOL
$SRC_VOL/testScripts/startup.sh
