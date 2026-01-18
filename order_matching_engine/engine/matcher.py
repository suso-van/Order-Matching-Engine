class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book

    def process_order(self, order):
        """
        Entry point for all orders.
        Matching logic will be implemented here.
        """
        raise NotImplementedError("Matching logic not implemented yet")
