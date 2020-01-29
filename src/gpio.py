import json
import time
import RPi.GPIO as GPIO

import utils

class GpioHelper:
    def __init__(self, sensors_list):
        if not sensors_list:
            raise ValueError("At least one sensor must be given")

        self.PINS = {}

        for sensor in sensors_list:
            self.PINS[sensor['pin']] = sensor['name']

        GPIO.setmode(GPIO.BCM)

        for pin in self.PINS.keys():
            GPIO.setup(pin, GPIO.IN)

    def start_listening(self, callback):
        for pin in self.PINS.keys():
            utils.log("Adding GPIO listener on {pin}".format(pin=pin))
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

        utils.log("Waiting for motion detection")

    def stop_listening(self):
        utils.log("Quitting motion detection...")
        GPIO.cleanup()
        utils.log("GPIO event detection stopped & cleaned")

    @staticmethod
    def is_rising(pin):
        return bool(GPIO.input(pin))
