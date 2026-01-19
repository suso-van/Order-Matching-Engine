from collections import defaultdict, deque
from models.enums import Side

class OrderBook:
    def __init__(self):
        self.buy_orders = defaultdict(deque)
        self.sell_orders = defaultdict(deque)

    def add_order(self, order):
        book = self.buy_orders if order.side == Side.BUY else self.sell_orders
        book[order.price].append(order)

    def best_bid(self):
        return max(self.buy_orders) if self.buy_orders else None

    def best_ask(self):
        return min(self.sell_orders) if self.sell_orders else None

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
