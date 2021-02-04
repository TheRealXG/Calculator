FROM ubuntu:18.04
RUN	apt-get update && \
	 apt-get install -y --no-install-recommends sudo \
	 qemu-system \
	 git \
	 python-dev \
	 pax \
	 binutils \
	 gcc \
	 g++ \
	 gdb \
	 unzip \
	 python2.7-dev \
	 curl \
	 python3-pip
RUN	sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/Chicago" apt-get build-dep -y binutils gcc g++ gdb unzip git python2.7-dev pax
RUN mkdir -p /rtems/quick-start/src && \
	mkdir -p /usr/tmp
WORKDIR /rtems/quick-start/src
RUN curl https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-source-builder-5.1.tar.xz | tar xJf - && \
	mv rtems-source-builder-5.1 rsb && \
	curl https://ftp.rtems.org/pub/rtems/releases/5/5.1/sources/rtems-5.1.tar.xz | tar xJf - 
WORKDIR /rtems/quick-start/src/rsb/rtems
RUN ../source-builder/sb-set-builder --prefix=/rtems/quick-start/rtems/5 5/rtems-arm
RUN	../source-builder/sb-set-builder --prefix=/rtems/quick-start/rtems/5 \ 
		--target=arm-rtems5 --with-rtems-bsp=realview_pbx_a9_qemu --with-rtems-tests=yes 5/rtems-kernel 
RUN pip3 install robotframework docutils
RUN pip3 install --upgrade robotframework-datadriver
COPY ./usr/tmp /usr/tmp
RUN chmod +x /usr/tmp/start.sh
CMD ["/usr/tmp/start.sh"]