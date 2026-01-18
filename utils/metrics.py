import time

class Metrics:
    def __init__(self):
        self.start_time = time.time()
        self.orders_processed = 0

    def record_order(self):
        self.orders_processed += 1

    def summary(self):
        elapsed = time.time() - self.start_time
        return {
            "orders_processed": self.orders_processed,
            "elapsed_time_sec": elapsed
        }
