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
# setup GPIO pins
#
GPIO.setmode(GPIO.BCM)

PINS = {}
if configs.A_PIN is not None:
    PINS[configs.A_PIN] = configs.A_NAME
if configs.B_PIN is not None:
    PINS[configs.B_PIN] = configs.B_NAME

for pin in PINS.keys():
    GPIO.setup(pin, GPIO.IN)

#
# setup mqtt client, then
# initialize mqtt connection & begin loop
#
mqtt = MqttHelper(configs).connect()

#
# With MQTT connection established, handle PIR sensor
#
def motion(pin_returned):
    sensor_id = PINS[pin_returned]
    if sensor_id is None:
        raise ValueError("The returnec pin is invalid")

    topic = "security/motion_sensors/" + sensor_id
    utils.log("motion detected, sending mqtt event to {topic}".format(topic=topic))
    res = {
        'timestamp': utils.timestamp(),
        'message': "motion detected at {sensor_id}".format(sensor_id=sensor_id),
        'motion': True
    }

    mqtt.publish(topic, json.dumps(res))

try:
    for pin in PINS.keys():
        utils.log("Adding GPIO listener on {pin}".format(pin=pin))
        GPIO.add_event_detect(pin, GPIO.RISING, callback=motion)

    utils.log("Waiting for motion detection")
    while 1:
        time.sleep(3600)

except KeyboardInterrupt:
    utils.log("\nQuitting motion detection...")
    GPIO.cleanup()
    utils.log("GPIO event detection stopped & cleaned")

    mqtt.disconnect()
