def build_sensor(sensor):
    sensor['type'] = sensor.get('type', 'default')
    types = {
        'motion': MotionSensor,
        'door': ReedSwitch,
        'window': ReedSwitch,
    }

    return types.get(sensor['type'], Sensor)(sensor)

class Sensor:
    def __init__(self, data):
        self.name = data['name']
        self.type = data['type']
        self.group = data['group']
        self.pin = data['pin']
        self.topic = self.group + '/' + self.type + '/' + self.name

    @staticmethod
    def determine_state(rising):
        return "TRIPPED" if rising else "OK"

class MotionSensor(Sensor):
    pass

class ReedSwitch(Sensor):
    @staticmethod
    def determine_state(rising):
        return "OK" if rising else "TRIPPED"
