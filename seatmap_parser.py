from src.parser.seatmap1_parser import SeatMap1Parser
from src.writer.json_writer import JsonWriter

seats = SeatMap1Parser().parse('seatmap1.xml')
JsonWriter().write('seatmap1.json', seats)
