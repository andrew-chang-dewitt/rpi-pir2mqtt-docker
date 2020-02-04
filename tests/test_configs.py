import pytest

from src.configs import Configs

class TestConfigs:
    config_contents =  '''

'''
def test_load():
    loaded = Configs.load('asdf')

    assert loaded == "asdf"
