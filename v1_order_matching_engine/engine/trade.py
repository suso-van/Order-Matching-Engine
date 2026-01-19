class Trade:
    def __init__(self, buy_id, sell_id, price, quantity):
        self.buy_id = buy_id
        self.sell_id = sell_id
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"TRADE {self.quantity}@{self.price} (B:{self.buy_id} S:{self.sell_id})"
