#!/usr/bin/env python3

# 
# import dependencies
# 
import os
import time
from datetime import datetime
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# 
# basic logger
#
def timestamp():
  return datetime.now().isoformat()

def log(msg):
  print(timestamp() + ": " + msg)

# 
# setup GPIO pin
# 
PIR_PIN = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# 
# setup mqtt client
# 
MQTT_HOST = os.getenv('MQTT_HOST', "127.0.0.1")
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

mqtt.Client.connected_flag = False # creates connection flag for looping
mqttc = mqtt.Client("living room motion")

#
# initialize mqtt connection & begin loop
# 
def on_connect(client, userdata, flags, rc):
  if rc==0:
    client.connected_flag=True
    log("Connection established to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
  else: 
    log("Connection failed to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
    log("Failure reason code: {rc}".format(rc=rc))

mqttc.on_connect = on_connect # binding client connection callback to above fn

mqttc.loop_start()
log("Attempting to establish connection to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
mqttc.connect(MQTT_HOST, MQTT_PORT)

while not mqttc.connected_flag:
  log("Waiting for connection")
  time.sleep(1)

#
# With MQTT connection established, handle PIR sensor
#
SENSOR_ID = os.getenv('SENSOR_ID', 'test_sensor')
topic = "security/motion_sensors/" + SENSOR_ID
def motion(PIR_PIN):
  log("motion detected, sending mqtt event to {topic}".format(topic=topic))
  res = {
    'timestamp': timestamp(),
    'message': "motion detected at {SENSOR_ID}".format(
        SENSOR_ID=SENSOR_ID
    ),
    'motion': True
  }

  mqttc.publish(topic, json.dumps(res))

try:
  log("Adding GPIO listener on {PIR_PIN}".format(PIR_PIN=PIR_PIN))
  GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
  log("Waiting for motion detection")
  while 1:
    time.sleep(3600)
#
# Use KeyboardInterrupt as quit signal to cleanup GPIO & MQTT loop
except KeyboardInterrupt:
  log("\nQuitting motion detection...")
  GPIO.cleanup()
  log("GPIO event detection stopped & cleaned")

  mqttc.loop_stop()
  mqttc.disconnect()
  log("MQTT client disonnected")
