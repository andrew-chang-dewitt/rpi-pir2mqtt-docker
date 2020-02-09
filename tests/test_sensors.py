import pytest

from src.sensors import build_sensor, Sensor, MotionSensor, ReedSwitch
import factories


def test_can_create_a_Sensor_from_dict():
    raw = factories.SENSOR_A
    raw['group'] = 'a group'
    sensor = build_sensor(raw)

    assert isinstance(sensor, Sensor)
    assert sensor.type == 'motion'
    assert sensor.name == 'sensor_a'
    assert sensor.pin == 7
    assert sensor.group == 'a group'


@pytest.fixture
def default_sensor() -> Sensor:
    return factories.Sensor.create_type(None)


@pytest.fixture
def motion() -> MotionSensor:
    return factories.Sensor.create_type('motion')


@pytest.fixture
def door() -> ReedSwitch:
    return factories.Sensor.create_type('door')


@pytest.fixture
def window() -> ReedSwitch:
    return factories.Sensor.create_type('window')


def test_if_no_type_is_given_default_to_Sensor(default_sensor):
    assert isinstance(default_sensor, Sensor)


def test_if_an_unknown_type_is_given_default_to_Sensor():
    unknown_sensor = factories.Sensor.create_type('a new type')
    assert isinstance(unknown_sensor, Sensor)


def test_default_sensor_returns_TRIPPED_if_rising(default_sensor):
    assert default_sensor.determine_state(
        factories.mock_gpio_input_rising_fn) == 'TRIPPED'


def test_motion_sensor_returns_TRIPPED_if_rising(motion):
    assert motion.determine_state(
        factories.mock_gpio_input_rising_fn) == 'TRIPPED'


def test_window_sensors_return_TRIPPED_if_falling(window):
    assert window.determine_state(
        factories.mock_gpio_input_falling_fn) == 'TRIPPED'


def test_door_sensors_return_TRIPPED_if_falling(door):
    assert door.determine_state(
        factories.mock_gpio_input_falling_fn) == 'TRIPPED'


def test_sensors_typically_dont_need_pull_up_down_resistors(default_sensor):
    assert not default_sensor.pull_up
    assert not default_sensor.pull_down


def test_door_window_sensors_need_pull_down_resistors(door, window):
    assert not window.pull_up
    assert window.pull_down
    assert not door.pull_up
    assert door.pull_down
