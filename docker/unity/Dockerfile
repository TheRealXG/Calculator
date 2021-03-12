FROM ubuntu:18.04
RUN	apt-get update && \
	 apt-get install -y --no-install-recommends gcc \
	 build-essential \
	 ruby \
	 python3-pip \
	 python3-pkg-resources \
	 python3-setuptools 
RUN mkdir -p /usr/tmp
RUN gem install ceedling
RUN pip3 install gcovr
COPY ./usr/tmp /usr/tmp
RUN chmod +x /usr/tmp/start.sh
CMD ["/usr/tmp/start.sh"]
