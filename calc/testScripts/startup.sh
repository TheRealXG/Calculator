#!/bin/bash

#set enviromental variables for SDK
. ./environment-setup-x86_64-wrlinuxsdk-linux
. ./oe-init-build-env build
. /home/wrlbuild/wrl-sdk/environment-setup-ppc7400-wrs-linux
export LANG=en_US.UTF-8

#add calc package to platform
echo "IMAGE_INSTALL_append += \" calc\"" >> /home/wrlbuild/wrl/build/conf/local.conf

#copy source to bitbake local bitbake layers location
mkdir -p /home/wrlbuild/wrl/layers/local/recipes-sample/calc
cp -R /volume/* /home/wrlbuild/wrl/layers/local/recipes-sample/calc

#for some reason repodata folder isn't empty, maually remove it
rm -R /home/wrlbuild/wrl/build/tmp-glibc/work/qemuppc-wrs-linux/wrlinux-image-small/1.0-r1/oe-rootfs-repo/repodata
#rebuild image
bitbake wrlinux-image-small

#Run the Robot test framework on all *.robot files in testScripts. Output in main Calculator folder.
cd /volume/calc
robot --xunit results testScripts/.

#debug statements
echo "Startup.sh script was ran." >> /volume/log.txt
