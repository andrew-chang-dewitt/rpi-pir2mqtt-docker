#!/usr/bin/env python3

#
# import dependencies
#
import time
import json
import RPi.GPIO as GPIO

import configs
import utils
from mqtt import MqttHelper

#
# basic logging utilities
#
#
# setup GPIO pin
#
PIR_PIN = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

#
# setup mqtt client, then
# initialize mqtt connection & begin loop
#
mqtt = MqttHelper(configs).connect()

#
# With MQTT connection established, handle PIR sensor
#
SENSOR_ID = os.getenv('SENSOR_ID', 'test_sensor')
topic = "security/motion_sensors/" + SENSOR_ID
def motion(PIR_PIN):
    log("motion detected, sending mqtt event to {topic}".format(topic=topic))
    res = {
        'timestamp': timestamp(),
        'message': "motion detected at {SENSOR_ID}".format(SENSOR_ID=SENSOR_ID),
        'motion': True
    }

    mqttc.publish(topic, json.dumps(res))

try:
    log("Adding GPIO listener on {PIR_PIN}".format(PIR_PIN=PIR_PIN))
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
    log("Waiting for motion detection")
    while 1:
        time.sleep(3600)
except KeyboardInterrupt:
    log("\nQuitting motion detection...")
    GPIO.cleanup()
    log("GPIO event detection stopped & cleaned")

    mqtt.disconnect()
