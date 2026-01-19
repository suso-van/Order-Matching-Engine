import time
import threading

class Metrics:
    def __init__(self):
        self.start_time = time.perf_counter()
        self.lock = threading.Lock()

        self.orders_processed = 0
        self.trades_executed = 0
        self.total_latency = 0.0

    def record_order(self, latency):
        with self.lock:
            self.orders_processed += 1
            self.total_latency += latency

    def record_trade(self):
        with self.lock:
            self.trades_executed += 1

    def summary(self):
        elapsed = time.perf_counter() - self.start_time
        avg_latency = (
            self.total_latency / self.orders_processed
            if self.orders_processed > 0 else 0
        )

        return {
            "orders_processed": self.orders_processed,
            "trades_executed": self.trades_executed,
            "elapsed_time_sec": round(elapsed, 4),
            "throughput_ops_sec": round(self.orders_processed / elapsed, 2)
                if elapsed > 0 else 0,
            "avg_latency_ms": round(avg_latency * 1000, 4),
        }
