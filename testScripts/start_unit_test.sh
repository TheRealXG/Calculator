#!/bin/bash

#Check to see if SRC_VOL is set, if not, default to /volume
if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

cd $SRC_VOL

#fix Symlinks from git repo if necessary
#some files that arent links are valid code files... so only convert to link if the first line contains "../*S"
ls -d1 src/* | while read f; do
  if [ ! -L "$f" ]; then
    IFS= read -r line < "$f" || [ -n "$line" ] || continue
    case $line in
      ("../"*) ln -sf "$(cat $f)" "$f"
    esac
  fi
done

#run Ceedling
ceedling gcov:all utils:gcov

#run gcov again... to get the .gcov files.....
gcov -o build/gcov/out gen/*.c
gcov -o build/gcov/out man/*.c
mkdir -p gcov
mv *.gcov gcov

echo "start_unit_test.sh scrip was run." >> $SRC_VOL/ut_log.txt
