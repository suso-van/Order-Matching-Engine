from engine.order_book import OrderBook
from engine.matcher import MatchingEngine
from models.order import Order
from models.enums import Side

def test_fifo_fairness():
    book = OrderBook()
    engine = MatchingEngine(book)

    engine.process_order(Order(1, Side.SELL, 100, 5))
    engine.process_order(Order(2, Side.SELL, 100, 5))
    engine.process_order(Order(3, Side.BUY, 100, 7))

    trades = engine.trades

    assert trades[0].sell_id == 1
    assert trades[1].sell_id == 2
