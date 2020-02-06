import json
import time
import RPi.GPIO as GPIO

from src import utils
from src import sensors


class GpioHelper:
    def __init__(self, sensors_list):
        self.input = GPIO.input

        if not sensors_list:
            raise ValueError("At least one sensor must be given")

        self.PINS = []
        GPIO.setmode(GPIO.BCM)

        for (pin, sensor) in sensors_list.items():
            self.PINS.append(pin)

            if sensor.pull_up or sensor.pull_down:
                if sensor.pull_up:
                    pull_up_down = GPIO.PUD_UP
                elif sensor.pull_down:
                    pull_up_down = GPIO.PUD_DOWN

                GPIO.setup(
                    pin,
                    GPIO.IN,
                    pull_up_down=pull_up_down)
            else:
                GPIO.setup(pin, GPIO.IN)

    def start_listening(self, callback):
        for pin in self.PINS:
            utils.log("Adding GPIO listener on {pin}".format(pin=pin))
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

        utils.log("Waiting for motion detection")

    def stop_listening(self):
        utils.log("Quitting motion detection...")
        GPIO.cleanup()
        utils.log("GPIO event detection stopped & cleaned")
