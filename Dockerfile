FROM armhf/alpine:latest
MAINTAINER Andrew Chang-DeWitt

#
# Install build-deps, python3, & pip packages
#
Run apk add --no-cache --virtual build-deps alpine-sdk python3-dev && \
  apk add --no-cache python3 && \
  pip3 install --upgrade pip && \
  pip3 install RPi.GPIO paho-mqtt

#
# Copy python script
#
RUN mkdir -p /app
COPY app /app
RUN chmod +x /app/sense.py

#
# Remove build-deps
#
Run apk del build-deps

#
# Set entrypoint to python script
#
ENTRYPOINT ["/app/sense.py"]
# ENTRYPOINT ["/bin/sh"]
