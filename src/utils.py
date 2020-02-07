"""Module exporting shared functions.

Functions:
    timestamp -- For getting the current time in an ISO string.
    log       -- For logging to stdout
"""

from datetime import datetime


def timestamp():
    """Return a string representing the current date/time in ISO format."""
    return datetime.now().isoformat()


def log(msg):
    """Wrap the print builtin adding a timestamp at the beginning."""
    print(timestamp() + ": " + msg)
