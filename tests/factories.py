from src.sensors import build_sensor
from src.sensors import Sensor as SensorActual

class Sensor:
    @staticmethod
    def create():
        return build_sensor({
            'name': 'a sensor',
            'group': 'a group',
            'pin': 1,
        })

    @staticmethod
    def create_type(str: type) -> SensorActual:
        return build_sensor({
            'name': 'a sensor',
            'group': 'a group',
            'type': type,
            'pin': 1,
        })
