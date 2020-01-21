#!/usr/bin/env python3

# 
# import dependencies
# 
import os
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

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
    print("Connection established to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
  else: 
    print("Connection failed to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
    print("Failure reason code: {rc}".format(rc=rc))

mqttc.on_connect = on_connect # binding client connection callback to above fn

mqttc.loop_start()
print("Attempting to establish connection to MQTT Host @ {MQTT_HOST}:{MQTT_PORT}".format(MQTT_HOST=MQTT_HOST, MQTT_PORT=MQTT_PORT))
mqttc.connect(MQTT_HOST, MQTT_PORT)

while not mqttc.connected_flag:
  print("Waiting for connection")
  time.sleep(1)

#
# With MQTT connection established, handle PIR sensor
#
SENSOR_ID = os.getenv('SENSOR_ID', 'test_sensor')
topic = "security/motion_sensors/" + SENSOR_ID
def motion(PIR_PIN):
  print("motion detected, sending mqtt event to {topic}".format(topic=topic))
  mqttc.publish(topic, "detected")

try:
  print("Adding GPIO listener on {PIR_PIN}".format(PIR_PIN=PIR_PIN))
  GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
  print("Waiting for motion detection")
  while 1:
    time.sleep(3600)
#
# Use KeyboardInterrupt as quit signal to cleanup GPIO & MQTT loop
except KeyboardInterrupt:
  print("\nQuitting motion detection...")
  GPIO.cleanup()
  print("GPIO event detection stopped & cleaned")

  mqttc.loop_stop()
  mqttc.disconnect()
  print("MQTT client disonnected")
