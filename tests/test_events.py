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
    assert event.log() == 'state on name, sending mqtt message'

@pytest.fixture
def fault():
    return factories.Fault.create()

def test_fault_is_an_Event(fault):
    assert isinstance(fault, Event)

def test_fault_always_names_the_event_FAULT_STATE(fault):
    assert fault.name == 'fault_state'

def test_fault_guards_only_accepts_FAILED_or_OK_as_state():
    with pytest.raises(ValueError) as excinfo:
        Fault('invalid value', 'time is a lie')

    assert 'is not a valid input for `fault_signal()' in str(excinfo.value)
