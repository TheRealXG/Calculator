FROM windriver/ubuntu1804_64
# RUN	apt-get update && \
	# DEBIAN_FRONTEND="noninteractive" TZ="America/Chicago" apt-get install -y --no-install-recommends \
	# sudo \
	# gawk \
	# wget \
	# git-core \
	# diffstat \
	# unzip \
	# texinfo \
	# gcc-multilib \
	# build-essential \
	# chrpath \
	# socat \
	# cpio \
	# python \
	# python3 \
	# python3-pip \
	# python3-pexpect \
	# xz-utils \
	# debianutils \
	# iputils-ping libsdl1.2-dev \
	# xterm
RUN mkdir -p /home/wrlbuild/wrl
WORKDIR /home/wrlbuild/wrl
RUN git clone --branch WRLINUX_10_19_BASE https://github.com/WindRiver-Labs/wrlinux-x
RUN ./wrlinux-x/setup.sh --machines qemuppc
RUN . ./environment-setup-x86_64-wrlinuxsdk-linux
RUN . ./oe-init-build-env
RUN sed -i "s/BB_NO_NETWORK ?= '1'/BB_NO_NETWORK ?= '0'/g" /home/wrlbuild/wrl/build/conf/local.conf
RUN sed -i 's/WRTEMPLATE ?= ""/WRTEMPLATE ?= "feature\/gdb"/g' /home/wrlbuild/wrl/build/conf/local.conf
RUN echo "SDKMACHINE = \"x86_64\"" >> /home/wrlbuild/wrl/build/conf/local.conf
#RUN echo "WRTEMPLATE ?= "calc"" >> /~/wrl/build/conf/local.conf
#WORKDIR /home/wrlbuild/wrl/build/
#RUN export LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8 && . ./oe-init-build-env && bitbake wrlinux-image-small
RUN export LANG=en_US.UTF-8 && . ./environment-setup-x86_64-wrlinuxsdk-linux && . ./oe-init-build-env && bitbake -c  populate_sdk wrlinux-image-small
RUN ./build/tmp-glibc/deploy/sdk/wrlinux-10.19.45.15-glibc-x86_64-qemuppc-wrlinux-image-small-sdk.sh -d ~/wrl-sdk -y
RUN sudo pip3 install robotframework docutils
RUN sudo pip3 install --upgrade robotframework-datadriver
COPY ./usr/tmp /usr/tmp
RUN sudo chmod +x /usr/tmp/start.sh
CMD ["/usr/tmp/start.sh"]