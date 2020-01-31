import json
import time
import RPi.GPIO as GPIO

import utils
import sensors

class GpioHelper:
    def __init__(self, sensors_list):
        if not sensors_list:
            raise ValueError("At least one sensor must be given")

        self.PINS = []
        GPIO.setmode(GPIO.BCM)

        for (pin, sensor) in sensors_list.items():
            self.PINS.append(pin)

            if isinstance(sensor, sensors.ReedSwitch):
                GPIO.setup(
                    pin,
                    GPIO.IN,
                    pull_up_down=GPIO.PUD_DOWN)
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

    @staticmethod
    def is_rising(pin):
        return bool(GPIO.input(pin))
