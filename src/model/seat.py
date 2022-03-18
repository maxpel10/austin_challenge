from src.model.price import Price


class Seat:
    def __init__(self, id: str, row: int, column: int, location:str, availability: bool,  cabin_class: str, features: list, price: Price):
        self.id = id
        self.row = row
        self.column = column
        self.location = location
        self.availability = availability
        self.cabin_class = cabin_class
        self.features = features
        self.price = price

    def toJson(self):
        return{
            "id": self.id,
            "row": self.row,
            "column": self.column,
            "location": self.location,
            "availability": self.availability,
            "cabin_class": self.cabin_class,
            "features": self.features,
            "price": self.price.toJson()
        }
