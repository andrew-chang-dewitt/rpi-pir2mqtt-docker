import pytest

import factories
from src.events import Event, Fault

@pytest.fixture
def event():
    return factories.Event.create()

def test_an_event_can_be_extracted_as_a_dict(event):
    assert event.as_dict() == {
        'name': 'name',
        'state': 'state',
        'timestamp': 'time is a lie'
    }

def test_an_event_can_be_extracted_as_json(event):
    json = event.as_json()

    assert 'name' in json
    assert 'state' in json
    assert 'time is a lie' in json

def test_event_can_create_a_log_string(event):
    assert event.log() == "state on name, sending mqtt message"
