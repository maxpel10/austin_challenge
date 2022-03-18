from ..model.price import Price
from ..model.seat import Seat
import xml.etree.ElementTree as ET


class SeatMap2Parser():
    # Namespaces from the xml file
    __ns = {
        'ns': 'http://www.iata.org/IATA/EDIST/2017.2',
        'ns2': 'http://www.iata.org/IATA/EDIST/2017.2/CR129',
    }

    # Dictionary to convert a column letter to a column number
    __columnMapper = {
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7
    }

    # Dictionary to convert a Seat Definition for seat availability to a value
    __availibilityValues = {"SD4": True, "SD19": False}

    # Dictionary to convert a Seat Definition for cabin class. I use a dictionary because I think the cabin class types can increase
    __cabinClassValues = {"SD16": "PREFERENTIAL"}

    # List which contains the location seats definitions
    __locationValues = ["SD3", "SD5"]

    # Method for transform a xml to a list of seats objects
    def parse(self, file) -> list:
        # Get the root of the xml element tree
        xml_root = ET.parse(file).getroot()
        # Get the prices values from the ALaCarteOffer xml tag
        prices_info = self.__getPricesInfo(xml_root)
        # Get the all the seat definitions values from the SeatDefinitionList xml tag
        seats_definition = self.__getSeatsDefinition(xml_root)
        # Get a list of dictionaries, where every dictionary represent a cabin, which has a column positions and an list of rows
        cabins_info = self.__getCabinsInfo(xml_root)
        # Get a list of seats objects
        seats = self.__getSeats(cabins_info, prices_info, seats_definition)
        # Return the list of seats objects
        return seats

    # Returns the prices values from the ALaCarteOffer xml tag
    def __getPricesInfo(self, root):
        prices_info = {}
        prices = root.find(
            'ns:ALaCarteOffer', self.__ns).findall('ns:ALaCarteOfferItem', self.__ns)
        for p in prices:
            priceId = p.get('OfferItemID')
            priceValue = p.find('ns:UnitPriceDetail', self.__ns).find(
                'ns:TotalAmount', self.__ns).find('ns:SimpleCurrencyPrice', self.__ns)
            prices_info[priceId] = Price(
                float(priceValue.text), priceValue.get('Code'))
        return prices_info

    # Returns the all the seat definitions values from the SeatDefinitionList xml tag
    def __getSeatsDefinition(self, root):
        seats_definition = {}
        definitions = root.find(
            'ns:DataLists', self.__ns).find(
            'ns:SeatDefinitionList', self.__ns).findall('ns:SeatDefinition', self.__ns)
        for d in definitions:
            definitionId = d.get('SeatDefinitionID')
            definitionValue = d.find('ns:Description', self.__ns).find(
                'ns:Text', self.__ns)
            seats_definition[definitionId] = definitionValue.text
        return seats_definition

    # Returns a list of dictionaries, where every dictionary represent a cabin, which has a column positions and an list of rows
    def __getCabinsInfo(self, root):
        cabins_info = []
        seat_maps = root.findall('ns:SeatMap', self.__ns)
        for s in seat_maps:
            cabin = s.find('ns:Cabin', self.__ns)
            columns_positions = self.__getColumnsPositions(cabin)
            rows = cabin.findall('ns:Row', self.__ns)
            cabins_info.append(
                {'columns_positions': columns_positions, 'rows': rows})
        return cabins_info

    # Returns a dictionary where the keys are column letter and the value is a string location, in a specific cabin
    def __getColumnsPositions(self, cabin):
        columns_positions = {}
        cabin_layout = cabin.find('ns:CabinLayout', self.__ns)
        columns = cabin_layout.findall('ns:Columns', self.__ns)
        for c in columns:
            # If the column hasn't text, I assume it's because it's a center position
            columns_positions[c.get('Position')
                              ] = c.text != '' and c.text or 'CENTER'
        return columns_positions

    # Returns a list of seats objects
    def __getSeats(self, cabins_info, prices_info, seats_definition):
        seats = []
        for cabin_info in cabins_info:
            columns_positions = cabin_info['columns_positions']
            rows = cabin_info['rows']
            for r in rows:
                seat_info = r.findall('ns:Seat', self.__ns)
                for s in seat_info:
                    seat = self.__getSeat(
                        r, s, prices_info, seats_definition, columns_positions)
                    seats.append(seat)
        return seats

    # Returns an individual seat object
    def __getSeat(self, row_info, seat, prices_info, seats_definitions, columns_positions):
        row = int(row_info.find('ns:Number', self.__ns).text)
        column_letter = seat.find('ns:Column', self.__ns).text
        column = self.__columnMapper[column_letter]
        id = str(row)+column_letter
        location = columns_positions[column_letter]
        availability, cabin_class,  features = self.__getInfoFromFeatures(
            seat, seats_definitions)
        price = self.__getPrice(seat, prices_info)
        return Seat(id, row, column, location, availability, cabin_class, features, price)

    # Returns cabin class, availability and features from a seat
    def __getInfoFromFeatures(self, seat, seats_definitions):
        # Default values
        cabin_class = "ECONOMY"
        availability = False
        features = []

        seat_definitions_refs = seat.findall('ns:SeatDefinitionRef', self.__ns)

        # Analize the seat definition info
        for sdr in seat_definitions_refs:
            feature = sdr.text
            # If the feature is a availability feature
            if(feature in self.__availibilityValues.keys()):
                # It's assigned
                availability = self.__availibilityValues[feature]
            else:
                # If the feature is a cabin class feature
                if(feature in self.__cabinClassValues.keys()):
                    # It's assigned
                    cabin_class = self.__cabinClassValues[feature]
                else:
                    # If the feature is a location feature
                    if (feature in self.__locationValues):
                        # It's ignored
                        pass
                    else:
                        # It's added to the list of features
                        features.append(seats_definitions[feature])
        return (availability, cabin_class, features)

    # Returns the price of a seat
    def __getPrice(self, seat, prices_info):
        price = Price(0.0, 'USD')
        offer_item_ref = seat.find('ns:OfferItemRefs', self.__ns)
        if(offer_item_ref != None):
            price = prices_info[offer_item_ref.text]
        return price
