#!/bin/bash

if [ -z "$SRC_VOL" ]; then
  export SRC_VOL="/volume"
fi

cppcheck --xml man/ gen/
