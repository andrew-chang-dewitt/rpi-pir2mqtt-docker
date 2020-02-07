"""Main file for running the rpi-security-gpio2mqtt module.

Classes:
    App -- a class that exposes modules to run the application

Functions:
    error_handler  -- handles Exceptions & allows the App to gracefully quit
    sig_handler    -- a callback given to the signal lib

Runs the application in a try...except statement to capture Exceptions
& allow for graceful exits.
"""

#
# import dependencies
#
import time
import signal
from typing import Callable, Any

from src import utils
from src.configs import load_configs
from src.mqtt import MqttHelper
from src.gpio import GpioHelper
from src.events import Event, Fault


class App:
    """Set up other modules & handles imperitive code for running application.

    Methods:
    run  -- runs the application in a loop & handles events
    quit -- sends a quit signal that stops the loop in run()
    """

    def __init__(
            self,
            external_error_handler:
            Callable[Exception, Callable[[Any], Any], None]):
        """Set up an Application instance.

        Initialize other modules' classes & set up instance state.

        Arguments:
        external_error_handler -- a function to handle errors that may arise
                                  inside the application, must accept an
                                  Exeption & a callback
        """
        # initilize running variable for tracking quit state
        self.__exit = False

        self.__error_handler = external_error_handler

        # load configuration
        self.__configs = load_configs('/app/configuration.yaml')

        # setup GPIO pins
        self.__gpio = GpioHelper(self.__configs.sensor_list)

        # setup mqtt client, then
        # initialize mqtt connection & begin loop
        self.__mqtt = MqttHelper(
            self.__configs.mqtt_host,
            self.__configs.mqtt_port).connect()

        self.__fault_signal("FAILED")

    def run(self):
        """Run the application."""
        def __cb(pin_returned):
            # wrap callback in a try/except that rethrows errors to the main
            # thread so that the app doesn't keep chugging along thinking
            # everything is okay
            try:
                return self.__event_detected(pin_returned)
            except Exception as err:  # pylint: disable=broad-except
                self.__error_handler(err, self.quit)

        self.__gpio.start_listening(__cb)

        while not self.__exit:
            self.__fault_signal("OK")
            time.sleep(600)

    def quit(self):
        """Quit the application & performs cleanup for a graceful exit."""
        self.__exit = True

        # cleanup
        self.__fault_signal("FAILED")
        self.__gpio.stop_listening()
        self.__mqtt.disconnect()
        utils.log("rpi-pir2mqtt successfully shut down")

    def __event_detected(self, pin_returned):
        sensor = self.__configs.sensor_list[pin_returned]
        topic = self.__configs.root_topic + sensor.topic
        state = sensor.determine_state(self.__gpio.input)
        event = Event(topic, state, utils.timestamp())

        utils.log(event.log())
        self.__mqtt.publish(topic, event.as_json())

    def __fault_signal(self, fault_state):
        topic = self.__configs.root_topic + "fault"
        event = Fault(fault_state, utils.timestamp())

        utils.log(event.log())
        self.__mqtt.publish(topic, event.as_json())


def error_handler(exception, callback):
    """Very very basic error "handler".

    Arguments:
    exception -- the exception being handled
    callback  -- a function to call before simply re-raising
                 the original exception
    """
    utils.log("An unexpected error has occurred, exiting app...")
    callback()
    raise exception


def sig_handler(signo, _frame):
    """Log signal & pass handling to App.quit().

    Simple callback to be given to signal.signal().
    """
    utils.log(
        "sig_handler processing {signo} signal"
        .format(signo=signo))
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
except Exception as err:  # pylint: disable=broad-except
    error_handler(err, APP.quit())
