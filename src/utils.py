from datetime import datetime


def timestamp():
    return datetime.now().isoformat()


def log(msg):
    print(timestamp() + ": " + msg)
