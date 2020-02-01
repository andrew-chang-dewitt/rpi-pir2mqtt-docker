#!/usr/bin/env python3
"""
Entry script for the rpi-security-gpio2mqtt
application. covers actually running the app
as well as very rudimentary error handling
"""

#
# import dependencies
#
import time
import json
import signal

import utils
from configs import Configs
from mqtt import MqttHelper
from gpio import GpioHelper

class App:
    """
    The Application itself is housed here.
    Inits and stores helper classes as well as
    the app data as instance variables
    """

    def __init__(self, err_handler):
        """
        Application constructor, accepts an
        error handler function to stored as
        an instance variable available
        throughout the running application.

        Also inits helper classes and begins
        setting them up.

        Lastly, inits an instance variable for
        signaling an exit request as False.
        Changing this to True tells the app
        to exit.
        """
        # initilize running variable for tracking quit state
        self.exit = False

        self.error_handler = err_handler

        # load configuration
        self.config = Configs.load('/src/configuration.yaml')

        # setup GPIO pins
        self.gpio = GpioHelper(self.config.sensor_list)

        # setup mqtt client, then
        # initialize mqtt connection & begin loop
        self.mqtt = MqttHelper(
            self.config.mqtt_host,
            self.config.mqtt_port).connect()

        self.fault_signal("FAILED")

    def event_detected(self, pin_returned):
        """
        An instance method passed to a callback
        for RPi.GPIO's event detection method.
        Setting it up as an instance method
        passed to the callback allows access to
        `self` while keeping the method in
        which the callback is needed
        uncluttered.

        The core purpose of this method is to
        send MQTT messages signaling sensor
        state on GPIO events.
        """

        sensor = self.config.sensor_list[pin_returned]
        topic = self.config.root_topic + sensor.topic
        state = sensor.determine_state(self.gpio.is_rising(pin_returned))

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
            'state': state,
            'sensor_data': sensor,
            'timestamp': utils.timestamp(),
        }

        self.mqtt.publish(topic, json.dumps(res), retain=True)

    def fault_signal(self, fault_state):
        """
        Used to set and publish the cureent app
        status. If sending "OK", the app is
        running as expected, but if a "FAILED"
        is sent, then the app is broadcasting
        that it is currently unable to process
        the sensors correctly and is unreliable
        """

        if fault_state in ("FAILED", "OK"):
            state = fault_state
        else:
            raise ValueError("'{fault_state}' is not a valid input for `fault_signal()`")

        topic = self.config.root_topic + "fault"
        res = {
            'id': 'fault',
            'state': state,
            'timestamp': utils.timestamp(),
        }

        utils.log(
            "fault state set to {state}, "
            "sending mqtt event to {topic}"
            .format(
                state=state,
                topic=topic,
            )
        )

        self.mqtt.publish(topic, json.dumps(res), retain=True)

    def run(self):
        """
        Used to run the application.

        Defines a callback that delegates to
        the `event_detected` method above for
        multi-threaded handling of GPIO events,
        then initiates GPIO event listeners
        with said callback and starts a loop to
        wait for events.
        """
        def callback(pin_returned):
            """
            wrap callback in a try/except that
            rethrows errors to the main thread
            so that the app doesn't keep
            chugging along thinking everything
            is okay
            """
            try:
                return self.event_detected(pin_returned)
            # pylint: disable=broad-except
            except Exception as err:
                self.error_handler(err, self.quit)

        self.gpio.start_listening(callback)

        while not self.exit:
            self.fault_signal("OK")
            time.sleep(600)


    def quit(self):
        """
        Kills the loop started in `run()` by
        setting the `exit` variable to True,
        Then signals a system failure and
        performs system cleanup.
        """
        self.exit = True

        # cleanup
        self.fault_signal("FAILED")
        self.gpio.stop_listening()
        self.mqtt.disconnect()
        utils.log("rpi-pir2mqtt successfully shut down")

def error_handler(exception, callback):
    """
    an overly simplified error handler. used as
    a global method to allow access before an
    `App' instance is even initiated.`
    """
    utils.log("An unexpected error has occurred, exiting app...")
    callback()
    raise exception

def sig_handler(_signo, _frame):
    """
    A callback to referr modified signal
    handlers to `App.quit()`
    """
    utils.log("sig_handler processing quit signal")
    APP.quit()

APP = App(error_handler)
signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

try:
    utils.log("Starting app...")
    APP.run()
except SystemExit:
    utils.log("SystemExit caught, quitting...")
    APP.quit()
except Exception as err: # pylint: disable=broad-except
    error_handler(err, APP.quit())
