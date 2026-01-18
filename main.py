from engine.order_book import OrderBook
from models.order import Order
from models.enums import Side

if __name__ == "__main__":
    book = OrderBook()

    book.add_order(Order(1, Side.BUY, 100.0, 10))
    book.add_order(Order(2, Side.SELL, 101.0, 5))
    book.add_order(Order(3, Side.BUY, 100.0, 7))

    print(book)
