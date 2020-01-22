import json
import time
import RPi.GPIO as GPIO

import utils

class GpioHelper:
    def __init__(self, sensor_A, sensor_B=None):
        if sensor_A is None and sensor_B is None:
            raise ValueError("At least one sensor must be given")

        self.PINS = {}
        self.PINS[sensor_A["pin"]] = sensor_A["name"]

        if sensor_B is not None:
            self.PINS[sensor_B["pin"]] = sensor_B["name"]

        GPIO.setmode(GPIO.BCM)

        for pin in self.PINS.keys():
            GPIO.setup(pin, GPIO.IN)

        self.listeners = []

    def add_listener(self, rising, callback):
        self.listeners.append({
            'direction' : rising,
            'callback' : callback
        })

    def listen(self):
        for pin in self.PINS.keys():
            utils.log("Starting GPIO listeners on {pin}".format(pin=pin))

            for listener in self.listeners:
                direction = GPIO.RISING if listener['direction'] else GPIO.FALLING
                utils.log(
                    "trying to add {direction} to {pin}"
                    .format(
                        direction=listener['direction'],
                        pin=pin))

                GPIO.add_event_detect(pin, direction, callback=listener['callback'])
                utils.log("{direction} listener started".format(direction=direction))

        utils.log("Waiting for motion detection")
        while 1:
            time.sleep(3600)

    def stop(self):
        utils.log("\nQuitting motion detection...")
        GPIO.cleanup()
        utils.log("GPIO event detection stopped & cleaned")
