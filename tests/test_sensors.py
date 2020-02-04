import pytest

from src.sensors import build_sensor, Sensor, MotionSensor, ReedSwitch

@pytest.fixture
def raw_sensor_motion():
    return {
        'type': 'motion',
        'name': 'sensor',
        'group': 'a group',
        'pin': 7,
    }

def test_can_create_a_Sensor_from_dict(raw_sensor_motion):
    sensor = build_sensor(raw_sensor_motion)

    assert isinstance(sensor, Sensor)
    assert sensor.type == 'motion'
    assert sensor.name == 'sensor'
    assert sensor.pin == 7

def test_motion_sensors_are_of_the_right_subclass(raw_sensor_motion):
    assert isinstance(build_sensor(raw_sensor_motion), MotionSensor)

def test_door_sensors_are_of_the_right_subclass(raw_sensor_motion):
    raw_door = raw_sensor_motion
    raw_door['type'] = 'door'

    assert isinstance(build_sensor(raw_door), ReedSwitch)

def test_window_sensors_are_of_the_right_subclass(raw_sensor_motion):
    raw_window = raw_sensor_motion
    raw_window['type'] = 'window'

    assert isinstance(build_sensor(raw_window), ReedSwitch)

def test_if_no_type_is_given_default_to_Sensor(raw_sensor_motion):
    default = raw_sensor_motion
    del default['type']

    assert isinstance(build_sensor(default), Sensor)
