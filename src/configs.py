import yaml

from sensors import build_sensor

class Configs:
    def __init__(self, config_obj):
        self.mqtt_host = config_obj['mqtt_host']
        self.mqtt_port = config_obj['mqtt_port']
        self.root_topic = config_obj['root_topic']

        self.sensor_list = {}

        for (group, sensor_list) in config_obj['sensor_groups'].items():
            for sensor in sensor_list:
                sensor['group'] = group
                self.sensor_list[sensor['pin']] = build_sensor(sensor)

    @staticmethod
    def load(config_file):
        with open(config_file, 'r') as stream:
            try:
                return Configs(yaml.safe_load(stream))
            except:
                raise
