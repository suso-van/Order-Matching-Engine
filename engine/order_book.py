from collections import defaultdict, deque
from models.enums import Side

class OrderBook:
    def __init__(self):
        self.buy_orders = defaultdict(deque)   # price -> FIFO queue
        self.sell_orders = defaultdict(deque)

    def add_order(self, order):
        if order.side == Side.BUY:
            self.buy_orders[order.price].append(order)
        else:
            self.sell_orders[order.price].append(order)

    def __repr__(self):
        return (
            f"BUY: {dict(self.buy_orders)}\n"
            f"SELL: {dict(self.sell_orders)}"
        )
