import pytest

from .src.configs import Configs

CONFIG_CONTENTS = '''
mqtt_host: "127.0.0.1"
mqtt_port: 1883
root_topic: "/security/sensors/"

sensor_groups:
    example_group:
      - name: "sensor_a"
        type: "motion"
        pin: 7
      - name: "sensor_B"
        type: "door"
        pin: 8
    another_group:
      - name: "sensor_1"
        type: "window"
        pin: 9
'''

@pytest.fixture
def config_file(tmp_path):
    config_file = tmp_path / "config_file.yaml"
    config_file.write_text(CONFIG_CONTENTS)

    return config_file

@pytest.fixture
def loaded(config_file):
    return Configs.load(str(config_file))

def test_can_load_configuration_file(loaded):
    assert isinstance(loaded, Configs)

def test_a_loaded_config_file_has_root_attributes(loaded):
    assert loaded.mqtt_host == "127.0.0.1"
    assert loaded.mqtt_port == 1883
    assert loaded.root_topic == "/security/sensors/"

def test_a_loaded_config_file_loads_all_sensors(loaded):
    assert len(loaded.sensor_list) == 3
