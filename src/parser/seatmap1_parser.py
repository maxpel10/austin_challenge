from src.model.price import Price
from src.model.seat import Seat
import xml.etree.ElementTree as ET


class SeatMap1Parser():
    # Namespaces from the xml file
    __ns = {
        'soapenc': "http://schemas.xmlsoap.org/soap/encoding/",
        'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'ns': "http://www.opentravel.org/OTA/2003/05/common/"
    }

    # Method for transform a xml to a list of seats objects
    def parse(self, file) -> list:
        # Get all the rows from the xml
        rows_info = self.__getRowsInfo(file)
        # Get all the seats
        seats = self.__getSeats(rows_info)
        # Return the list of seats objects
        return seats

    # Returns the element tree with tag ns:RowInfo
    def __getRowsInfo(self, file):
        rows_info = []
        # ElementTree converts a XML file into a tree data structure where we can find the differents tags using the namespaces from the xml
        cabins_class = ET.parse(file).getroot().find('soapenv:Body', self.__ns).find('ns:OTA_AirSeatMapRS', self.__ns).find(
            'ns:SeatMapResponses', self.__ns).find('ns:SeatMapResponse', self.__ns).find('ns:SeatMapDetails',  self.__ns).findall('ns:CabinClass', self.__ns)
        # For every cabin class, get the rows
        for c in cabins_class:
            rows_info += c.findall('ns:RowInfo', self.__ns)
        return rows_info

    # Returns  the list of seats objects
    def __getSeats(self, rows_info):
        seats = []
        for r in rows_info:
            seat_info = r.findall('ns:SeatInfo', self.__ns)
            for s in seat_info:
                seats.append(self.__getSeat(r, s))
        return seats

    # Returns an individual seat object from the ns:SeatInfo and ns:RowInfo tags
    def __getSeat(self, row_info, seat):
        summary = seat.find('ns:Summary', self.__ns)
        id = summary.get('SeatNumber')
        row = int(row_info.get('RowNumber'))
        column = int(seat.get('ColumnNumber'))
        location, features = self.__getFeatures(seat)
        availability = summary.get('AvailableInd') == "false" and False or True
        cabin_class = row_info.get('CabinType').upper()
        price = self.__getPrice(seat)
        return Seat(id, row, column, location, availability, cabin_class, features, price)

    # Returns the seat location
    def __getFeatures(self, seat):
        location = None
        features = []
        fts = seat.findall('ns:Features', self.__ns)
        for f in fts:
            if(f.text != "Other_"):
                if(f.text == "Window" or f.text == "Aisle" or f.text == "Center"):
                    location = f.text.upper()
                else:
                    features.append(f.text.upper())
            else:
                features.append(f.get('extension').upper())
        return location, features

    # Returns the price object from the seat
    def __getPrice(self, seat):
        service = seat.find('ns:Service', self.__ns)
        # Default values
        seat_fee = 0.0
        seat_taxes = 0.0
        currency = "USD"
        if(service != None):
            fee = service.find('ns:Fee', self.__ns)
            if(fee != None):
                seat_fee = float(fee.get('Amount'))
                currency = fee.get('CurrencyCode')
                taxes = fee.find('ns:Taxes')
                if(taxes != None):
                    seat_taxes = float(taxes.get('amount'))
        # amount = fee + taxes
        return Price(seat_fee+seat_taxes, currency)
