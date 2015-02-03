import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below
def get_avg_latlng():
	data = readCSV("permits_hydepark.csv") 
	number = 0.0
	longitude = 0.0
	latitude = 0.0
	for datum in data:
		longitude += float(line[-2]) 
		latitude += float(line[-3])
		number += 1.0
	return latitude/number, longitude/number
