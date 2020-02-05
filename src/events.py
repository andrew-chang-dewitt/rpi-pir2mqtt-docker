import json

class Event:
    def __init__(self, name: str, state: str, timestamp: str):
        self.name = name
        self.state = state
        self.timestamp = timestamp

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'state': self.state,
            'timestamp': self.timestamp
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    def log(self) -> str:
        return ("{state} on {name}, "
                "sending mqtt message"
                .format(
                    state=self.state,
                    name=self.name,))

class Fault:
    def __init__(self, name: str, fault_state: str, timestamp: str):
        if fault_state == "FAILED" or fault_state == "OK":
            state = fault_state
        else:
            raise ValueError("'{fault_state}' is not a valid input for `fault_signal()`")

        self.name = name
        self.state = state
        self.timestamp = timestamp
