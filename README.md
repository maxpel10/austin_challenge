# Austin Software Challenge
Author: Maximiliano Pellegrino

Python version:  3.9.6

## Input
```  
py seatmap_parser.py [FILENAME]
```
## Output
You will get a .json file in the same directory as the original file, with the same file name. This file will contain the list of seats obtained from the xml file.

**Seat json format:**
```
{
	"id": "12C",
	"row": 12,
	"column": 3,
	"location": "AISLE",
	"availability": true,
	"cabin_class": "ECONOMY",
	"features": [
		"SEAT_NOT_SUITABLE_FOR_CHILD",
		"SEAT_NOT_ALLOWED_FOR_INFANT",
		"RESTRICTED_RECLINE_SEAT",
		"WING",
		"SEAT_NOT_ALLOWED_FOR_MEDICAL",
		"EXIT",
		"LEG_SPACE_SEAT"
	],
	"price": {
	"amount": 35.4,
	"currency": "GBP"
	}
},
```

## Detail
- If the seat price and location doesn't exist, the json corresponding field will be null.
