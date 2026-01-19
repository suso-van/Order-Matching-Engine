from collections import defaultdict, deque
from models.enums import Side

class OrderBook:
    def __init__(self):
        self.buy_orders = defaultdict(deque)
        self.sell_orders = defaultdict(deque)

    def add_order(self, order):
        if order.side == Side.BUY:
            self.buy_orders[order.price].append(order)
        else:
            self.sell_orders[order.price].append(order)

    def best_bid(self):
        return max(self.buy_orders.keys()) if self.buy_orders else None

    def best_ask(self):
        return min(self.sell_orders.keys()) if self.sell_orders else None

    def pop_best_buy(self):
        price = self.best_bid()
        order = self.buy_orders[price].popleft()
        if not self.buy_orders[price]:
            del self.buy_orders[price]
        return order

    def pop_best_sell(self):
        price = self.best_ask()
        order = self.sell_orders[price].popleft()
        if not self.sell_orders[price]:
            del self.sell_orders[price]
        return order

    def validate(self):
        for price, queue in self.buy_orders.items():
            for o in queue:
                assert o.price == price
                assert o.quantity > 0

        for price, queue in self.sell_orders.items():
            for o in queue:
                assert o.price == price
                assert o.quantity > 0

    def __repr__(self):
        return f"BUY: {dict(self.buy_orders)}\nSELL: {dict(self.sell_orders)}"
