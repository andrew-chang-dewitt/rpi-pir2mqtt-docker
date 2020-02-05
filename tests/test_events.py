import pytest

from src.events import Event, Fault

def test_can_create_an_Event():
    assert Event()
