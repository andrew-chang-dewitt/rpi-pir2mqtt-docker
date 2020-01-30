FROM armhf/alpine:latest
# fix arm build issues on x86 platforms
# COPY qemu-arm-static /usr/bin

MAINTAINER Andrew Chang-DeWitt

#
# Install build-deps, python3, & pip packages
#
Run apk add --no-cache --virtual build-deps alpine-sdk python3-dev && \
  apk add --no-cache python3 && \
  pip3 install --upgrade pip && \
  pip3 install RPi.GPIO paho-mqtt PyYAML

#
# Copy python script
#
RUN mkdir -p /src
COPY src /src
RUN chmod +x /src/sense.py

#
# Remove build-deps
#
Run apk del build-deps

#
# Set entrypoint to python script
#
ENTRYPOINT ["/src/sense.py"]
# ENTRYPOINT ["/bin/sh"]
