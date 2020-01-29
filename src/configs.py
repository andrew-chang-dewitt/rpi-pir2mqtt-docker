import yaml

class Config:
    def __init__(self, config_obj):
        self.mqtt_host = config_obj['mqtt_host']
        self.mqtt_port = config_obj['mqtt_port']
        self.root_topic = config_obj['root_topic']

        self.sensors = {}

        for (group, sensors) in config_obj['sensor_groups'].items():
            for sensor in sensors:
                sensor['group'] = group
                self.sensors[sensor['pin']] = sensor

    @staticmethod
    def load(config_file):
        with open(config_file, 'r') as stream:
            try:
                return Config(yaml.safe_load(stream))
            except:
                raise
