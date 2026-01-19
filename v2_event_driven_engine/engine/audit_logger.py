import json

class AuditLogger:
    def __init__(self, file_path="data/audit.log"):
        self.file_path = file_path
        open(self.file_path, "a").close()

    def log(self, audit_event):
        with open(self.file_path, "a") as f:
            f.write(json.dumps(audit_event.to_record()) + "\n")
            f.flush()

