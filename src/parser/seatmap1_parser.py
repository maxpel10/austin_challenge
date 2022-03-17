from ..model.price import Price
from ..model.seat import Seat
import xml.etree.ElementTree as ET


class SeatMap1Parser():
    # Name spaces defined by soap
    __ns = {
        'soapenc': "http://schemas.xmlsoap.org/soap/encoding/",
        'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'ns': "http://www.opentravel.org/OTA/2003/05/common/"
    }

    def parse(self, file):
        rows_info = self.__getRowsInfo(file)
        seats = self.__getSeats(rows_info)
        return seats

    def __getRowsInfo(self, file):
        # ElementTree converts a XML file to a tree data structure where we can find the differents tags using the namespaces defined by soap
        rows_info = []
        cabins_class = ET.parse(file).getroot().find('soapenv:Body', self.__ns).find('ns:OTA_AirSeatMapRS', self.__ns).find(
            'ns:SeatMapResponses', self.__ns).find('ns:SeatMapResponse', self.__ns).find('ns:SeatMapDetails',  self.__ns).findall('ns:CabinClass', self.__ns)
        for c in cabins_class:
            rows_info += c.findall('ns:RowInfo', self.__ns)
        return rows_info

    def __getSeats(self, rows_info):
        seats = []
        for r in rows_info:
            seat_info = r.findall('ns:SeatInfo', self.__ns)
            for s in seat_info:
                seats.append(self.__getSeat(r, s))
        return seats

    def __getSeat(self, row_info, seat):
        summary = seat.find('ns:Summary', self.__ns)
        id = summary.get('SeatNumber')
        row = int(row_info.get('RowNumber'))
        column = int(seat.get('ColumnNumber'))
        availability = summary.get('AvailableInd') == "false" and False or True
        cabin_class = row_info.get('CabinType')
        features = self.__getFeatures(seat)
        price = self.__getPrice(seat)
        return Seat(id, row, column,availability, cabin_class, features, price)

    def __getFeatures(self, seat):
        return list(map(lambda f: f.text != 'Other_' and f.text or f.get('extension'),
                        seat.findall('ns:Features', self.__ns)))

    def __getPrice(self, seat):
        service = seat.find('ns:Service', self.__ns)
        seat_fee = 0.0
        fee_currency = "USD"
        seat_taxes = 0.0
        taxes_currency = "USD"

        if(service != None):
            fee = service.find('ns:Fee', self.__ns)
            if(fee != None):
                seat_fee = float(fee.get('Amount'))
                fee_currency = fee.get('CurrencyCode')
                taxes = fee.find('ns:Taxes')
                if(taxes != None):
                    seat_taxes = float(taxes.get('amount'))
                    taxes_currency = taxes.get('CurrencyCode')

        return Price(seat_fee, fee_currency, seat_taxes, taxes_currency)
