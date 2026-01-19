import time
from models.enums import Side, OrderStatus

class Order:
    def __init__(self, order_id, side, price, quantity):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
        self.status = OrderStatus.PENDING
        self.timestamp = time.time()

    def snapshot(self):
        return {
            "order_id": self.order_id,
            "side": self.side.value,
            "price": self.price,
            "quantity": self.quantity,
        }

    @staticmethod
    def from_snapshot(data):
        return Order(
            data["order_id"],
            Side(data["side"]),
            data["price"],
            data["quantity"],
        )

    def __repr__(self):
        return f"{self.side.value} {self.quantity}@{self.price} [{self.status.value}]"
