FROM ubuntu:18.04
RUN	apt-get update && \
	 apt-get install -y --no-install-recommends sudo \
	 qemu-system \
	 gdb \
	 curl \
	 python \
	 python3\
	 python3-pip
RUN mkdir -p /usr/tmp
RUN pip3 install robotframework docutils
RUN pip3 install --upgrade robotframework-datadriver
COPY ./usr/tmp /usr/tmp
RUN chmod +x /usr/tmp/start.sh
CMD ["/usr/tmp/start.sh"]
