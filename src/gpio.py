"""A wrapper on RPi.GPIO; handles setting up, reading, & tearing down pins.

Classes:
    GpioHelper -- A simplified wrapper on RPi.GPIO.
"""
from typing import Callable
import RPi.GPIO as io

from src import utils


class GpioHelper:
    """Simplified wrapper on RPi.GPIO. Handles setup & simplifies connections.

    Methods:
        start_listening -- Start listening for HIGH or LOW on all pins.
        stop_listening  -- Wrapper on the RPi.GPIO.cleanup method.
    """

    def __init__(self, sensors_list: dict):
        """Init a GpioHelper instance with the given sensors."""
        if not sensors_list:
            raise ValueError("At least one sensor must be given")

        self.__pins = []
        io.setmode(io.BCM)

        for (pin, sensor) in sensors_list.items():
            self.__pins.append(pin)

            if sensor.pull_up or sensor.pull_down:
                if sensor.pull_up:
                    pull_up_down = io.PUD_UP
                elif sensor.pull_down:
                    pull_up_down = io.PUD_DOWN

                io.setup(
                    pin,
                    io.IN,
                    pull_up_down=pull_up_down)
            else:
                io.setup(pin, io.IN)

    def start_listening(self, callback: Callable[[int], bool]):
        """Start listening for HIGH or LOW on all pins.

        Arguments:
            callback -- a function to be called when a GPIO event is detected.
        """
        for pin in self.__pins:
            utils.log("Adding GPIO listener on {pin}".format(pin=pin))
            io.add_event_detect(pin, io.BOTH, callback=callback)

        utils.log("Waiting for motion detection")

    @staticmethod
    def stop_listening():
        """Execute RPi.GPIO.cleanup method."""
        utils.log("Quitting motion detection...")
        io.cleanup()
        utils.log("GPIO event detection stopped & cleaned")

    @staticmethod
    def input():
        """Wrap & directly expose RPi.GPIO's input method."""
        return io.input()
