# This Dockerfile will create a build environment for RTEMS 6
# This will checkout a specific commit for RTEMS 6 and build the RTEMS kernel
# This will build RTEMS for the ARM architecture
# This dockerfile can then be run and pass in a BSP config and build command 
#   while mapped to the source code directory to build the application

From ubuntu:20.04
# FROM registry1.dso.mil/ironbank/redhat/ubi/ubi8:8.3
RUN	apt-get update && \
	apt-get install -y --no-install-recommends sudo \
	python \
	python-dev \
	git \
	gcc \
	g++ \
	make \
	flex \
	bison \
	unzip \
	patch \
	xz-utils
# Install this seaprately because it asks for timezone info
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/Chicago" apt-get install -y --no-install-recommends texinfo
RUN mkdir -p /development/src
WORKDIR /development/src
# Clone required RTEMS source and tool scripts and checkout to a known commit
RUN git clone git://git.rtems.org/rtems-source-builder.git rsb
WORKDIR /development/src/rsb
RUN git checkout 62363ba
WORKDIR /development/src
RUN git clone git://git.rtems.org/rtems.git 
WORKDIR /development/src/rtems
RUN git checkout fd639b8abf
# Run Source Builder to download tools and build RTEMS
WORKDIR /development/src/rsb/rtems
RUN ../source-builder/sb-set-builder --prefix=/development/rtems/6 6/rtems-arm
ENV PATH="/development/rtems/6/bin/:$PATH"
# Bootstrap RTEMS
WORKDIR /development/src/rtems
RUN ./bootstrap -c && ./rtems-bootstrap
# Install LIBBSD networking library
WORKDIR /development/src/
RUN git clone git://git.rtems.org/rtems-libbsd.git
WORKDIR rtems-libbsd
# Checkout 6-freebsd-12 branch (this is a known commit point that works)
RUN git checkout aef7a74b9
RUN git submodule init
RUN git submodule update rtems_waf

# Get rtems_waf for the build application
WORKDIR /tmp
RUN git clone git://git.rtems.org/rtems_waf.git

# Copy in startup script to check for environment variables and start the BSP build and the src code build
COPY config_compile.sh /usr/local/bin/config_compile.sh
# This assumes the top level source code directory has been mounted to /src
ENTRYPOINT ["config_compile.sh"]
CMD ["./waf"]
# Will need to have a script that will accept a BSP from the command line (with a libbsd option?) that will then run the BSP config and install commands including for LIBBSD, this will include:

# BSP
#cd ~/development/src/rtems
# Create config.ini
#./waf configure --prefix=$PREFIX
#./waf
#./waf install
# LIBBSD
#cd ~/development/src/rtems-libbsd
#./waf configure --prefix=$PREFIX  --rtems-bsps=arm/xilinx_zynq_a9_qemu  --buildset=buildset/default.ini
#./waf
#./waf install

# Now it is ready to compile, have a volume passed in that has the source code, rtems_waf (container provide this?), and a wscript, then it runs
#./waf configure --rtems=$HOME/development/rtems/6 --rtems-bsp=arm/xilinx_zynq_a9_qemu --rtems-libbsd=$HOME/development/rtems/6
#./waf clean build
