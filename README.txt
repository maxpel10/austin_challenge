Thanks for your interest in this position with Gordian
Software's API Integration team.

The next step in the interview process is to complete 
the exercise below. This is a practical challenge 
similar to real problems you would solve as part of 
this team.

Seatmap Availability Exercise:

Our goal is to parse seatmap information from XML 
files and create a JSON format that our customers 
can parse so that they can display any airline 
seatmap by integrating our format.

Desired behavior: 

Input: python seatmap_parser.py [FILENAME]

Output: FILENAME_parsed.json

Description:
Write a python script that parses the XML seatmap 
filesincluded in this folder (seatmap1.xml, 
seatmap2.xml) into a standardized JSON format 
that outputs the seatmap (by row) with the following 
properties at minimum:
	- Seat/Element type (Seat, Kitchen, Bathroom, etc)
	- Seat id (17A, 18A)
	- Seat price
	- Cabin class
	- Availability

Feel free to include any other properties in your 
JSON format that you think are relevant.

Please avoid the use of xml to json libraries/tools 
such as xmltodict, objectify and the like.


