import threading
import time
from engine.order_book import OrderBook
from engine.event_engine import EventDrivenMatchingEngine
from models.order import Order
from models.enums import Side

WAL = "data/events.wal"

book = OrderBook()
engine = EventDrivenMatchingEngine(book, WAL)

t = threading.Thread(target=engine.run)
t.start()

engine.submit(Order(1, Side.BUY, 100, 10))
engine.submit(Order(2, Side.SELL, 100, 5))
engine.submit(Order(3, Side.SELL, 100, 5))

time.sleep(0.3)
engine.stop()

print("\n=== LIVE TRADES ===")
for trade in engine.trades:
    print(trade)

print("\n=== RECOVERY ===")
recovered_book = OrderBook()
recovered_engine = EventDrivenMatchingEngine(recovered_book, WAL)
recovered_engine.event_store.replay(recovered_engine)

for trade in recovered_engine.trades:
    print(trade)
