from enum import Enum


class EventType(Enum):
    ORDER_SUBMITTED = "ORDER_SUBMITTED"
    TRADE_EXECUTED = "TRADE_EXECUTED"
    ORDER_CANCELED = "ORDER_CANCELED"


class OrderStatus(Enum):
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

    def can_transition(self, new_status):
        transitions = {
            OrderStatus.PENDING: {
                OrderStatus.PARTIALLY_FILLED,
                OrderStatus.COMPLETED,
                OrderStatus.CANCELED,
            },
            OrderStatus.PARTIALLY_FILLED: {
                OrderStatus.COMPLETED,
                OrderStatus.CANCELED,
            },
            OrderStatus.COMPLETED: set(),
            OrderStatus.CANCELED: set(),
        }
        return new_status in transitions[self]

    def assert_transition(self, new_status):
        if not self.can_transition(new_status):
            raise ValueError(
                f"Invalid OrderStatus transition {self.value} -> {new_status.value}"
            )


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"
