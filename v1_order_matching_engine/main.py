import threading
import random
import time
from engine.order_book import OrderBook
from engine.matcher import MatchingEngine
from models.order import Order
from models.enums import Side

book = OrderBook()
engine = MatchingEngine(book)

def burst_submit(thread_id, bursts, orders_per_burst):
    for b in range(bursts):
        for i in range(orders_per_burst):
            side = Side.BUY if random.random() < 0.5 else Side.SELL
            price = random.randint(95, 105)
            qty = random.randint(1, 10)
            order_id = f"{thread_id}-{b}-{i}"
            engine.process_order(Order(order_id, side, price, qty))
        # Simulate quiet period between bursts
        time.sleep(0.01)

THREADS = 6
BURSTS = 10
ORDERS_PER_BURST = 200

threads = []
start = time.perf_counter()

for t_id in range(THREADS):
    t = threading.Thread(
        target=burst_submit,
        args=(t_id, BURSTS, ORDERS_PER_BURST)
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.perf_counter()

print("\n===== STRESS TEST METRICS =====")
summary = engine.metrics.summary()
for k, v in summary.items():
    print(f"{k}: {v}")

print(f"wall_clock_time_sec: {round(end - start, 4)}")
