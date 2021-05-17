#!/bin/bash

# This should be executed from the mapped source code volume. This is mapped at container runtime to /src. WORKDIR to /src before ENTRYPOINT

# Assumes a BSP config.ini file in the source code top level directory
# Given a wscript file in the source code top level directory (also rtems_waf or not?)

# Extract the BSP from the top of config.ini file
cd /src
bsp=$(head -n 1 config.ini)
temp=${bsp#"["}
bsp=${temp%"]"}
echo $bsp

# Check if an environemnt variable was passed in for libsbsd library, if not then set a default
if [ -z "$LIBBSD" ]; then
  export LIBBSD="n"
fi

# Copy the config.ini and execute the BSP build and install commands
cp /src/config.ini /development/src/rtems/
cd /development/src/rtems/
./waf configure --prefix=/development/rtems/6
./waf
./waf install

# Build libbsd and install it if desired
if [ $LIBBSD == "y" ]
then
  cd /development/src/rtems-libbsd
  ./waf configure --prefix=/development/rtems/6 \
    --rtems-bsps=$bsp \
    --buildset=buildset/default.ini
  ./waf
  ./waf install
  libbsd_path="--rtems-libbsd=/development/rtems/6"
else
   libbsd_path=""
fi

# Copy in the rtems_waf directory to build the application
cd /src
cp -R /tmp/rtems_waf /src

# Need command to build the actual source code (possibly do this with the docker command and have the rest as config/setup script?)
./waf configure --rtems=/development/rtems/6 --rtems-bsp=$bsp $libbsd_path

# Execute either the default Docker CMD (./waf) or a passed in command (e.g. ./waf clean build)
exec "$@"
