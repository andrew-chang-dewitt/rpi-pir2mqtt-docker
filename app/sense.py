#!/usr/bin/env python3

#
# import dependencies
#
import time
import json
from threading import Event
import RPi.GPIO as GPIO

import configs
import utils
from mqtt import MqttHelper
from gpio import GpioHelper

exit = Event()
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
    topic = configs.TOPIC + sensor_id
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
    if fault_state == "FAILED" or fault_state == "OK":
        state = fault_state
    else:
        raise ValueError("'{fault_state}' is not a valid input for `fault_signal()`")

    topic = configs.TOPIC + "fault"
    res = {
        'id': 'fault',
        'state': state,
        'timestamp': utils.timestamp(),
    }

    utils.log(
        "fault state set to {state}"
        "sending mqtt event to {topic}"
        .format(
            state=state,
            topic=topic,
        )
    )

    mqtt.publish(topic, json.dumps(res), retain=True)

fault_signal("FAILED")

def main():
    # setup inside loop checking for
    # end signals
    while not exit.is_set():
        gpio.start(motion)
        fault_signal("OK")
        exit.wait(6000)

    # cleanup
    fault_signal("FAILED")
    gpio.stop()
    mqtt.disconnect()

def quit(signo, _frame):
    utils.log(
        "Interrupted by {signo}, shutting down"
        .format(signo=signo)
    )
    exit.set()

utils.log("{n} is __name__".format(n=__name__))

if __name__ == "__main__":
    import signal
    utils.log("Registering signal handlers")

    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(
            getattr(
                signal, 'SIG'+sig),
            quit
        )

        utils.log("Starting app")
    main()
