FROM ubuntu:18.04
RUN	apt-get update && \
	apt-get install -y --no-install-recommends sudo \
	python \
	python3
COPY ./usr/tmp /usr/tmp
RUN chmod +x /usr/tmp/start.sh
CMD ["/usr/tmp/start.sh"]
