#!/bin/bash

if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

cd $SRC_VOL

cppcheck --enable=all --output-file=cpp_check_log.txt gen man
flawfinder gen man >& flawfinder_log.txt

echo "start_static_analysis.sh scrip was run." >> $SRC_VOL/sa_log.txt
