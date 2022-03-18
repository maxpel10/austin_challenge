class Price:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

    def toJson(self):
        return {
            "amount": self.amount,
            "currency": self.currency,
        }
