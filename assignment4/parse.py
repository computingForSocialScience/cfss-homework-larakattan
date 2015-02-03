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
		longitude += float(datum[-2]) 
		latitude += float(datum[-3])
		number += 1.0
	return latitude/number, longitude/number

def zip_code_barchart():
	data = readCSV("permits.csv")
	contractor_zip = {}
	for datum in data: 
		zips = [datum[28], datum[35], datum[42], datum[49], datum[56], datum[63], datum[70], datum[77], datum[84], datum[91], datum[98], datum[105], datum[112], datum[119], datum[126]]
		for zipcode in all_zipcodes:
			if zipcode == "": 
				continue
			zipcode = zipcode.split("-") 
			zipcode = zipcode[0] 
			if zipcode not in contractor_zip: 
				contractor_zip[zipcode] = 1
			else: 
				contractor_zip[zipcode] += 1

	plt.bar(range(len(contractor_zip)), contractor_zip.values(), align='center')
	plt.xticks(range(len(contractor_zip)), contractor_zip.keys())
	plt.savefig('histogram_of_zipcodes.jpg')
	
if sys.argv[1] == "latlong":
	print get_avg_latlng()
elif sys.argv[1] == "hist":
	zip_code_barchart()
else: print "Error in input!"
