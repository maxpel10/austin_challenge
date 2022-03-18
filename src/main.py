import sys
from src.parser.seatmap1_parser import SeatMap1Parser
from src.parser.seatmap2_parser import SeatMap2Parser
from src.writer.json_writer import JsonWriter


class Main():
    def run(self):

        # Get the filename
        try:
            filename = str(sys.argv[1])
        except:
            # If there isn't a second argument
            print("Error. You didn't entered the name of the xml file.")
            return

       # Create the json writer
        writer = JsonWriter()

        # Create the json filename
        json_filename = filename.split('.')[0]+'.json'

        # Try to parse with SeatMap1Parser and write the file
        try:
            seats = SeatMap1Parser().parse(filename)
        except:
            seats = None

        # If SeatMap1Parser fail
        if(seats == None):
            # Try to parse with SeatMap2Parser and write the file
            try:
                seats = SeatMap2Parser().parse(filename)
            except:
                seats = None

        # If both parsers failed
        if(seats == None):
            # Print error
            print(
                "Parse error. The file doesn't exist or there is an error with the xml file format.")
            return

        # Try to write the file
        try:
            writer.write(json_filename, seats)
            print("Success. File "+json_filename+" created.")
        except:
            print(
                "Writer error. The file couldn't be created.")

        return
