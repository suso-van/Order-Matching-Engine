import time

class AuditEvent:
    def __init__(self, event_type, details):
        self.event_type = event_type
        self.details = details
        self.timestamp = time.time()

    def to_record(self):
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "details": self.details,
        }

