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
PIR_PIN = configs.A_PIN
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
def motion(pin):
    if pin == configs.A_PIN:
        sensor_id = configs.A_NAME
    elif pin == configs.B_PIN:
        sensor_id = configs.B_NAME
    else:
        throw ValueError("this should be impossible")

    topic = "security/motion_sensors/" + sensor_id
    utils.log("motion detected, sending mqtt event to {topic}".format(topic=topic))
    res = {
        'timestamp': utils.timestamp(),
        'message': "motion detected at {sensor_id}".format(sensor_id=sensor_id),
        'motion': True
    }

    mqtt.publish(topic, json.dumps(res))

try:
    utils.log("Adding GPIO listener on {PIR_PIN}".format(PIR_PIN=PIR_PIN))
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
    utils.log("Waiting for motion detection")
    while 1:
        time.sleep(3600)
except KeyboardInterrupt:
    utils.log("\nQuitting motion detection...")
    GPIO.cleanup()
    utils.log("GPIO event detection stopped & cleaned")

    mqtt.disconnect()
