import time

class Event:
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = time.time()
