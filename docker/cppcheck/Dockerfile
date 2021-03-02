FROM ubuntu:18.04
RUN	apt-get update && \
	apt-get install -y --no-install-recommends sudo \
	cppcheck
RUN	apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/Chicago"
RUN	mkdir -p /usr/tmp
COPY 	./usr/tmp /usr/tmp
RUN 	chmod +x /usr/tmp/start.sh
CMD 	["/usr/tmp/start.sh"]
