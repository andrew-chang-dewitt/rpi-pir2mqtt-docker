"""A module for defining Sensor types.

Classes:
    Sensor       -- Base Sensor class, all unknown types default to this.
    MotionSensor -- Subclass of Sensor, for HC-SR501 type PIR sensors.
    ReedSwitch   -- Subclass of Sensor, for basic door/window reed switches.

Functions:
    build_sensor -- Build & return a Sensor or subclass based from dict.
"""

from typing import Type, Callable


class Sensor:
    """Base Sensor class, all unknown types default to this.

    Attributes:
        name  -- Used in identifying it in user-facing applications
        type  -- Used in config to identify subclass for behavior
        group -- Used in user-facing applications
        pin   -- Identifies the sensor's GPIO pin # (by Broadcom definition)
        topic -- Compiled from name, type, & group; used for routing messages

    Methods:
        determine_state -- Identify if the sensor is 'TRIPPED' or 'OK'.

    Properties:
        pull_up   -- Read-only, tells if sensor requires pull up resistor.
        pull_down -- Read-only, tells if sensor requires pull down resistor.
    """

    def __init__(self, data: dict):
        """Init a Sensor with attributes built from data's keys."""
        self.name = data['name']  # type: str
        self.type = data['type']  # type: str
        self.group = data['group']  # type: str
        self.pin = data['pin']  # type: int
        self.topic = (
            self.group + '/' +
            self.type + '/' +
            self.name)  # type: str

    def determine_state(
            self, check_state_callback: Callable[[int], bool]) -> str:
        """Identify if the sensor is 'TRIPPED' or 'OK'."""
        return "TRIPPED" if check_state_callback(self.pin) else "OK"

    @property
    def pull_up(self):
        """Read-only attribute, tells if sensor requires pull up resistor."""
        return False

    @property
    def pull_down(self):
        """Read-only attribute, tells if sensor requires pull down resistor."""
        return False


class MotionSensor(Sensor):
    """Subclass of Sensor, for HC-SR501 type PIR sensors.

    Currently has no different behavior from Sensor.
    """


class ReedSwitch(Sensor):
    """Subclass of Sensor, for basic door/window reed switches.

    Differs from Sensor in two ways:
    1. Returns 'OK' where the Sensor would return 'TRIPPED' & vice-versa
    2. Requires a pull up resistor
    """

    def determine_state(self, check_state_callback):
        """See Sensor.determine_state."""
        return "OK" if check_state_callback(self.pin) else "TRIPPED"

    @property
    def pull_up(self):
        """See Sensor.pull_up."""
        return True


def build_sensor(sensor: dict) -> Type[Sensor]:
    """Build & return a Sensor or subclass based from dict.

    Arguments:
        sensor -- A dict containing sensor information.
    """
    sensor_type = sensor.get('type', 'default')
    sensor['type'] = sensor_type if sensor_type is not None else 'default'
    types = {
        'motion': MotionSensor,
        'door': ReedSwitch,
        'window': ReedSwitch,
    }

    return types.get(sensor['type'], Sensor)(sensor)
