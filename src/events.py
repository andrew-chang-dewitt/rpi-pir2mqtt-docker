"""Events to be consumed by message sending or logging modules.

Classes:
    Event -- Generic event, tailored for basic state changes on named objects.
    Fault -- Subclass of event, intended for tracking application status.
"""
import json


class Event:
    """Generic event, tailored for basic state changes on named objects.

    Attributes:
        name      -- Identifies the object who's state is being broadcasted.
        state     -- Holds the new value for the object's state.
        timestamp -- An ISO timestamp for assisting in debugging.
    """

    def __init__(self, name: str, state: str, timestamp: str):
        """Init an Event object with given attributes."""
        self.name = name
        self.state = state
        self.timestamp = timestamp

    def as_dict(self) -> dict:
        """Return the Event formatted as a dictionary."""
        return {
            'name': self.name,
            'state': self.state,
            'timestamp': self.timestamp
        }

    def as_json(self) -> str:
        """Return the event formatted as a JSON string."""
        return json.dumps(self.as_dict())

    def log(self) -> str:
        """Return a log-friendly string representation of the Event."""
        return ("{state} on {name}, "
                "sending mqtt message"
                .format(
                    state=self.state,
                    name=self.name,))


class Fault(Event):
    """Subclass of event, intended for tracking application status.

    Differs only in defining the name to always be 'fault_state' & guarding
    the state value, must be either
        'FAILED', or
        'OK'
    """

    def __init__(self, fault_state: str, timestamp: str):
        """Init a Fault object with the given attributes."""
        if fault_state in ("FAILED", "OK"):
            state = fault_state
        else:
            raise ValueError(
                "'{fault_state}' is not a valid input for `fault_signal()`")

        self.name = 'fault_state'
        self.state = state
        self.timestamp = timestamp
