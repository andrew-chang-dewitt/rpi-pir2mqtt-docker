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
def motion(pin_returned):
    sensor_id = gpio.PINS[pin_returned]
    topic = configs.TOPIC + "/" + sensor_id
    motion = "MOTION" if gpio.is_rising(pin_returned) else "CLEAR"

    utils.log(
        "{motion} on pin {pin_returned}, "
        "sending mqtt event to {topic}"
        .format(
            motion=motion,
            pin_returned=pin_returned,
            topic=topic
        )
    )

    res = {
        'id' : sensor_id,
        'motion': motion,
        'timestamp': utils.timestamp(),
    }

    mqtt.publish(topic, json.dumps(res), retain=True)

def fault_signal(fault_state):
    res = "OK" if fault_state else "FAILED"

    utils.log(
        "fault state set to {res}"
        .format(
            res=res
        )
    )

    mqtt.publish(configs.TOPIC + "/fault", res, retain=True)

fault_signal(False)

try:
    gpio.listen(motion, fault_signal)

except KeyboardInterrupt:
    fault_signal(True)
    gpio.stop()
    mqtt.disconnect()
