from src.sensors import build_sensor
from src.sensors import Sensor as SensorActual
from src.configs import Configs as ConfigsActual
from src.events import Event as EventActual

def mock_gpio_input_rising_fn(pin_number):
    return 1

def mock_gpio_input_falling_fn(pin_number):
    return 0

SENSOR_A = {
    'name': 'sensor_a',
    'type': 'motion',
    'pin': 7,
}
SENSOR_B = {
    'name': 'sensor_b',
    'type': 'door',
    'pin': 8,
}
SENSOR_1 = {
    'name': 'sensor_1',
    'type': 'window',
    'pin': 9,
}

class Config:
    @staticmethod
    def create():
        return ConfigsActual({
            'mqtt_host': '127.0.0.1',
            'mqtt_port': 1883,
            'root_topic': '/security/sensors/',
            'sensor_groups': {
                'example_group': [SENSOR_A, SENSOR_B,],
                'another_group': [SENSOR_1,],
            }})

class Sensor:
    @staticmethod
    def create() -> SensorActual:
        sensor = SENSOR_A
        sensor['group'] = 'example_group'
        print("sensor", sensor)

        return build_sensor(sensor)

    @staticmethod
    def create_type(sensor_type: str) -> SensorActual:
        return build_sensor({
            'name': 'a sensor',
            'group': 'a group',
            'type': sensor_type,
            'pin': 1,
        })

class Event:
    @staticmethod
    def create() -> EventActual:
        return EventActual('name', 'state', 'time is a lie')
