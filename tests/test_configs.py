import pytest

import factories
from src.configs import Configs, ConfigsError, load_configs

CONFIG_CONTENTS = '''
mqtt_host: "127.0.0.1"
mqtt_port: 1883
root_topic: "/security/sensors/"

sensor_groups:
    example_group:
      - name: "sensor_a"
        type: "motion"
        pin: 7
      - name: "sensor_b"
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
    return load_configs(str(config_file))


@pytest.fixture
def configs(monkeypatch):
    monkeypatch.setenv('MQTT_USER', 'user')
    monkeypatch.setenv('MQTT_PASS', 'password')
    return factories.Configs.create()


@pytest.fixture
def no_auth(monkeypatch):
    monkeypatch.delenv('MQTT_USER', raising=False)
    monkeypatch.delenv('MQTT_PASS', raising=False)
    return factories.Configs.create()


def test_can_load_configuration_file(loaded):
    assert isinstance(loaded, Configs)


def test_a_loaded_config_has_root_attributes(configs):
    assert configs.mqtt_host == "127.0.0.1"
    assert configs.mqtt_port == 1883
    assert configs.mqtt_user == "user"
    assert configs.mqtt_pass == "password"
    assert configs.root_topic == "/security/sensors/"


def test_a_sensor_doesnt_require_mqtt_user_or_pass(no_auth):
    assert no_auth.mqtt_user is None
    assert no_auth.mqtt_pass is None


def test_a_user_must_have_both_user_and_pass_or_neither(monkeypatch):
    with pytest.raises(ConfigsError):
        monkeypatch.setenv('MQTT_USER', 'user')
        monkeypatch.delenv('MQTT_PASS', raising=False)
        factories.Configs.create()

    with pytest.raises(ConfigsError):
        monkeypatch.setenv('MQTT_PASS', 'password')
        monkeypatch.delenv('MQTT_USER', raising=False)
        factories.Configs.create()


def test_a_loaded_config_file_loads_all_sensors(configs):
    assert len(configs.sensor_list) == 3
