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
COPY app/sense.py /app/sense.py
RUN chmod +x /app/sense.py

#
# Set default environment variable values
# 
ENV MQTT_HOST="127.0.0.1"
ENV MQTT_PORT=1883
ENV SENSOR_ID="default_test"

#
# Remove build-deps
# 

Run apk del build-deps

#
# Set entrypoint to python script
# 

ENTRYPOINT ["/app/sense.py"]
# ENTRYPOINT ["/bin/sh"]
