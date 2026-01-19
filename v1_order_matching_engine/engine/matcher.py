import time
from engine.trade import Trade
from models.enums import Side
from concurrency.locks import OrderBookLock
from utils.metrics import Metrics

class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book
        self.trades = []
        self.lock = OrderBookLock()
        self.metrics = Metrics()

    def process_order(self, incoming):
        start = time.perf_counter()

        with self.lock:
            if incoming.side == Side.BUY:
                self._match_buy(incoming)
            else:
                self._match_sell(incoming)

        latency = time.perf_counter() - start
        self.metrics.record_order(latency)

    def _match_buy(self, buy):
        while buy.quantity > 0:
            best_ask = self.order_book.best_ask()
            if best_ask is None or buy.price < best_ask:
                break

            sell = self.order_book.pop_best_sell()
            qty = min(buy.quantity, sell.quantity)

            self.trades.append(
                Trade(buy.order_id, sell.order_id, sell.price, qty)
            )
            self.metrics.record_trade()

            buy.quantity -= qty
            sell.quantity -= qty

            if sell.quantity > 0:
                self.order_book.add_order(sell)

            self.order_book.validate()

        if buy.quantity > 0:
            self.order_book.add_order(buy)

    def _match_sell(self, sell):
        while sell.quantity > 0:
            best_bid = self.order_book.best_bid()
            if best_bid is None or sell.price > best_bid:
                break

            buy = self.order_book.pop_best_buy()
            qty = min(sell.quantity, buy.quantity)

            self.trades.append(
                Trade(buy.order_id, sell.order_id, buy.price, qty)
            )
            self.metrics.record_trade()

            sell.quantity -= qty
            buy.quantity -= qty

            if buy.quantity > 0:
                self.order_book.add_order(buy)

            self.order_book.validate()

        if sell.quantity > 0:
            self.order_book.add_order(sell)
