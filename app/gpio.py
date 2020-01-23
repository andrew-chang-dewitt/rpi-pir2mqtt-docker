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

    def listen(self, callback, fault_signal):
        for pin in self.PINS.keys():
            utils.log("Adding GPIO listener on {pin}".format(pin=pin))
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

        utils.log("Waiting for motion detection")

        while 1:
            fault_signal("OK")
            time.sleep(6000)

    def stop(self):
        utils.log("\nQuitting motion detection...")
        GPIO.cleanup()
        utils.log("GPIO event detection stopped & cleaned")

    @staticmethod
    def is_rising(pin):
        return bool(GPIO.input(pin))
