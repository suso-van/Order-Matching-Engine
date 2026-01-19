from models.order import Order
from engine.trade import Trade
from engine.events import EventType


class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)

    def replay(self, engine):
        for event in self.events:
            if event.event_type == EventType.ORDER_SUBMITTED:
                order = Order.from_snapshot(event.payload)
                engine.process(order)

            elif event.event_type == EventType.TRADE_EXECUTED:
                trade = Trade.from_snapshot(event.payload)
                engine.trades.append(trade)

            elif event.event_type == EventType.ORDER_CANCELED:
                engine.cancel_internal(event.payload["order_id"])
