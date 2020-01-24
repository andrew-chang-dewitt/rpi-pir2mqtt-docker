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

class App:
    def __init__(self):
        self.exit = Event() #
        # setup GPIO pins
        #
        self.gpio = GpioHelper(configs.SENSOR_A, configs.SENSOR_B)

        #
        # setup mqtt client, then
        # initialize mqtt connection & begin loop
        #
        self.mqtt = MqttHelper(configs).connect()
        self.fault_signal("FAILED")


    def motion(self, pin_returned):
        sensor_id = self.gpio.PINS[pin_returned]
        topic = configs.TOPIC + sensor_id
        state = "MOTION" if self.gpio.is_rising(pin_returned) else "CLEAR"

        utils.log(
            "{state} on pin {pin_returned}, "
            "sending mqtt event to {topic}"
            .format(
                state=state,
                pin_returned=pin_returned,
                topic=topic
            )
        )

        res = {
            'id' : sensor_id,
            'state': state,
            'timestamp': utils.timestamp(),
        }

        self.mqtt.publish(topic, json.dumps(res), retain=True)

    def fault_signal(self, fault_state):
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

        self.mqtt.publish(topic, json.dumps(res), retain=True)

    def main(self):
        def cb(pin_returned):
            return self.motion(pin_returned)

        while not self.exit.is_set():
            self.gpio.start(cb)
            self.fault_signal("OK")
            self.exit.wait()

        # cleanup
        self.fault_signal("FAILED")
        self.gpio.stop()
        self.mqtt.disconnect()

    def quit(self):
        def cb(signo, _frame):
            utils.log(
                "Interrupted by {signo}, shutting down"
                .format(signo=signo)
            )
            self.exit.set()

        return cb

utils.log("{n} is __name__".format(n=__name__))

if __name__ == "__main__":
    import signal

    app = App()

    utils.log("Registering signal handlers")

    signal.signal(
        signal.SIGINT,
        app.quit()
    )
    signal.signal(
        signal.SIGTERM,
        app.quit()
    )

    utils.log("Starting app")
    app.main()
