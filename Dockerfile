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
# Copy python app
#
RUN mkdir -p /app/src
COPY src /app/src
COPY configuration.yaml /app/configuration.yaml
RUN chmod +x /app/src/sense.py

#
# Remove build-deps
#
Run apk del build-deps

#
# Set entrypoint to python script
#
WORKDIR /app
ENTRYPOINT ["/usr/bin/python3", "-m", "src.sense"]
# ENTRYPOINT ["/bin/sh"]
