def build_sensor(sensor):
    sensor_type = sensor.get('type', 'default')
    sensor['type'] = sensor_type if sensor_type is not None else 'default'
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

    def determine_state(self, check_state_callback):
        return "TRIPPED" if check_state_callback(self.pin) else "OK"

    @property
    def pull_up(self):
        return False

    @property
    def pull_down(self):
        return False


class MotionSensor(Sensor):
    pass


class ReedSwitch(Sensor):
    def determine_state(self, check_state_callback):
        return "OK" if check_state_callback(self.pin) else "TRIPPED"

    @property
    def pull_up(self):
        return True
