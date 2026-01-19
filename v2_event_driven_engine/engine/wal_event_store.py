import json
from engine.events import EventType
from engine.event_log import Event
from models.order import Order
from engine.trade import Trade

class WALEventStore:
    def __init__(self, path):
        self.path = path
        open(self.path, "a").close()

    def append(self, event: Event):
        record = {
            "type": event.event_type.value,
            "payload": event.payload,
            "timestamp": event.timestamp,
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()

    def replay(self, engine):
        with open(self.path, "r") as f:
            for line in f:
                record = json.loads(line)
                etype = EventType(record["type"])

                if etype == EventType.ORDER_SUBMITTED:
                    engine.process(Order.from_snapshot(record["payload"]))

                elif etype == EventType.TRADE_EXECUTED:
                    engine.trades.append(
                        Trade.from_snapshot(record["payload"])
                    )

                elif etype == EventType.ORDER_CANCELED:
                    engine.cancel_internal(record["payload"]["order_id"])

