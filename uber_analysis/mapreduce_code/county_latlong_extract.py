import json
'''
extract polygon boundary lat-long for each county in NYC from a geojson file.
The geojson file is downloaded from 
http://catalog.opendata.city/dataset/new-york-counties-polygon/resource/c6540266-7bea-4c88-8deb-0ec6870c50b9
'''

with open('nyc_county_polygon.geojson') as f:
    data = json.load(f)

county_list = ['Bronx County, NY', 'Kings County, NY', 'Queens County, NY',
 'New York County, NY', 'Richmond County, NY']
for county in county_list:
	for feature in data['features']:
	    if feature['properties']['name'] == county:
	    	name = feature['properties']['name'].split(',')[0]
	    	coord =  feature['geometry']['coordinates'][0][0]

	f2 = open(name + '_polygon2.txt', 'w')
	for i in coord:
		f2.write('Point(%s, %s),' %(i[1], i[0]))
	f2.close()