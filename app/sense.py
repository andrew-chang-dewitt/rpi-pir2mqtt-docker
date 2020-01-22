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
from gpio import GpioHelper

#
# setup GPIO pins
#
gpio = GpioHelper(configs.SENSOR_A, configs.SENSOR_B)

#
# setup mqtt client, then
# initialize mqtt connection & begin loop
#
mqtt = MqttHelper(configs).connect()

#
# With MQTT connection established, handle PIR sensor
#
def motion_detected(pin_returned):
    sensor_id = gpio.PINS[pin_returned]
    topic = "security/motion_sensors/" + sensor_id

    utils.log(
        "change detected on pin {pin_returned}, "
        "sending mqtt event to {topic}"
        .format(
            pin_returned=pin_returned,
            topic=topic))
    res = {
        'timestamp': utils.timestamp(),
        'motion': gpio.is_rising(pin_returned)
    }

    mqtt.publish(topic, json.dumps(res))

def motion_stopped(pin_returned):
    sensor_id = gpio.PINS[pin_returned]
    if sensor_id is None:
        raise ValueError("The returned pin is invalid")

    topic = "security/motion_sensors/" + sensor_id
    utils.log(
        "motion stopped on pin {pin_returned}, "
        "sending mqtt event to {topic}"
        .format(
            pin_returned=pin_returned,
            topic=topic))
    res = {
        'timestamp': utils.timestamp(),
        'message': "motion stopped at {sensor_id}".format(sensor_id=sensor_id),
        'motion': False
    }

    mqtt.publish(topic, json.dumps(res))


try:
    gpio.listen(motion)

except KeyboardInterrupt:
    gpio.stop()
    mqtt.disconnect()
