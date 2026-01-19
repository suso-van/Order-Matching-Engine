class Trade:
    def __init__(self, buy_id, sell_id, price, quantity):
        self.buy_id = buy_id
        self.sell_id = sell_id
        self.price = price
        self.quantity = quantity

    def snapshot(self):
        return {
            "buy_id": self.buy_id,
            "sell_id": self.sell_id,
            "price": self.price,
            "quantity": self.quantity,
        }

    @staticmethod
    def from_snapshot(data):
        return Trade(
            data["buy_id"],
            data["sell_id"],
            data["price"],
            data["quantity"],
        )

    def __repr__(self):
        return f"TRADE {self.quantity}@{self.price} (B:{self.buy_id} S:{self.sell_id})"
