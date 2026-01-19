from queue import SimpleQueue
from engine.trade import Trade
from engine.event_log import Event
from engine.events import EventType
from engine.wal_event_store import WALEventStore
from engine.audit_logger import AuditLogger
from engine.audit_event import AuditEvent
from models.enums import Side, OrderStatus

class EventDrivenMatchingEngine:
    def __init__(self, order_book, wal_path):
        self.queue = SimpleQueue()
        self.order_book = order_book
        self.trades = []
        self.running = True
        self.event_store = WALEventStore(wal_path)
        self.audit = AuditLogger()

    def submit(self, order):
        self.event_store.append(
            Event(EventType.ORDER_SUBMITTED, order.snapshot())
        )
        self.audit.log(
            AuditEvent("ORDER_SUBMITTED", order.snapshot())
        )
        self.queue.put(order)

    def cancel(self, order_id):
        self.event_store.append(
            Event(EventType.ORDER_CANCELED, {"order_id": order_id})
        )
        self.audit.log(
            AuditEvent("ORDER_CANCELED", {"order_id": order_id})
        )
        self.cancel_internal(order_id)

    def run(self):
        while self.running:
            order = self.queue.get()
            self.process(order)

    def stop(self):
        self.running = False

    def process(self, order):
        if order.side == Side.BUY:
            self._match_buy(order)
        else:
            self._match_sell(order)

    def _emit_trade(self, trade):
        self.trades.append(trade)
        self.event_store.append(
            Event(EventType.TRADE_EXECUTED, trade.snapshot())
        )
        self.audit.log(
            AuditEvent("TRADE_EXECUTED", trade.snapshot())
        )

    def _match_buy(self, buy):
        while buy.quantity > 0:
            ask = self.order_book.best_ask()
            if ask is None or buy.price < ask:
                break

            sell = self.order_book.pop_best_sell()
            qty = min(buy.quantity, sell.quantity)

            self._emit_trade(
                Trade(buy.order_id, sell.order_id, sell.price, qty)
            )

            buy.quantity -= qty
            sell.quantity -= qty

            if sell.quantity > 0:
                sell.status = OrderStatus.PARTIALLY_FILLED
                self.order_book.add_order(sell)
            else:
                sell.status = OrderStatus.COMPLETED

        if buy.quantity > 0:
            buy.status = OrderStatus.PARTIALLY_FILLED
            self.order_book.add_order(buy)
        else:
            buy.status = OrderStatus.COMPLETED

    def _match_sell(self, sell):
        while sell.quantity > 0:
            bid = self.order_book.best_bid()
            if bid is None or sell.price > bid:
                break

            buy = self.order_book.pop_best_buy()
            qty = min(sell.quantity, buy.quantity)

            self._emit_trade(
                Trade(buy.order_id, sell.order_id, buy.price, qty)
            )

            sell.quantity -= qty
            buy.quantity -= qty

            if buy.quantity > 0:
                buy.status = OrderStatus.PARTIALLY_FILLED
                self.order_book.add_order(buy)
            else:
                buy.status = OrderStatus.COMPLETED

        if sell.quantity > 0:
            sell.status = OrderStatus.PARTIALLY_FILLED
            self.order_book.add_order(sell)
        else:
            sell.status = OrderStatus.COMPLETED

    def cancel_internal(self, order_id):
        for book in (self.order_book.buy_orders, self.order_book.sell_orders):
            for price in list(book.keys()):
                for order in list(book[price]):
                    if order.order_id == order_id:
                        order.status.assert_transition(OrderStatus.CANCELED)
                        order.status = OrderStatus.CANCELED
                        book[price].remove(order)
                        if not book[price]:
                            del book[price]
                        return
