import json
from locale import currency


class Price:
    def __init__(self, fee: float, fee_currency: str, taxes: float, taxes_currency:str):
        self.fee = fee
        self.fee_currency = fee_currency
        self.taxes = taxes
        self.taxes_currency = taxes_currency

    def toJson(self):
        return {
            "fee": self.fee,
            "fee_currency": self.fee_currency,
            "taxes": self.taxes,
            "taxes_currency": self.taxes_currency
        }