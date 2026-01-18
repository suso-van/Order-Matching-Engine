import time
from models.enums import Side

class Order:
    def __init__(self, order_id, side: Side, price: float, quantity: int):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
        self.timestamp = time.time()

    def __repr__(self):
        return f"{self.side.value} {self.quantity}@{self.price}"
