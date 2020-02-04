import pytest

from .src.sensors import build_sensor, Sensor, MotionSensor, ReedSwitch

@pytest.fixture
def raw_motion():
    return {
        'type': 'motion',
        'name': 'sensor',
        'group': 'a group',
        'pin': 7,
    }

@pytest.fixture
def raw_door():
    return {
        'type': 'door',
        'name': 'sensor',
        'group': 'a group',
        'pin': 7,
    }

@pytest.fixture
def raw_window():
    return {
        'type': 'window',
        'name': 'sensor',
        'group': 'a group',
        'pin': 7,
    }

@pytest.fixture
def default_sensor():
    return build_sensor({
        'name': 'sensor',
        'group': 'a group',
        'pin': 7,
    })


@pytest.fixture
def motion(raw_motion):
    return build_sensor(raw_motion)

@pytest.fixture
def door(raw_door):
    return build_sensor(raw_door)

@pytest.fixture
def window(raw_window):
    return build_sensor(raw_window)

def test_can_create_a_Sensor_from_dict(motion):
    assert isinstance(motion, Sensor)
    assert motion.type == 'motion'
    assert motion.name == 'sensor'
    assert motion.pin == 7

def test_motion_sensors_are_of_the_right_subclass(motion):
    assert isinstance(motion, MotionSensor)

def test_door_sensors_are_of_the_right_subclass(door):
    assert isinstance(door, ReedSwitch)

def test_window_sensors_are_of_the_right_subclass(window):
    assert isinstance(window, ReedSwitch)

def test_if_no_type_is_given_default_to_Sensor(default_sensor):
    assert isinstance(default_sensor, Sensor)
    assert not isinstance(default_sensor, MotionSensor)

def test_default_sensor_returns_TRIPPED_if_rising(default_sensor):
    rising = True

    assert default_sensor.determine_state(rising) == 'TRIPPED'

def test_motion_sensor_returns_TRIPPED_if_rising(motion):
    rising = True

    assert motion.determine_state(rising) == 'TRIPPED'

def test_door_and_window_sensors_return_TRIPPED_if_falling(door):
    rising = False

    assert door.determine_state(rising) == 'TRIPPED'
