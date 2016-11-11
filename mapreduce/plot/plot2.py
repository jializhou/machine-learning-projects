from spatial import *
import csv
import time
from county_latlong import * 


t1 = time.time()
with open('green-jun-2015.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	headers = ['Date/Time', 'Lat', 'Lon', 'District','Count']
	# reader.next()
	# ['Date/Time', 'Lat', 'Lon', 'District','Count']
	# reader.next()
	columns = {}
	for h in headers:
		columns[h] = []
	for row in reader:
		for h, v in zip(headers, row):
			columns[h].append(v)
csvfile.close()
length = len(columns['Lat'])
pts = []
for i in xrange(length):
	pts.append(Point(float(columns['Lat'][i]), float(columns['Lon'][i])))

idx = simpleRTree_insert(pts)

for j, Polys in enumerate(Polygon_lis):
	lb_x, lb_y = 50, 0
	rt_x, rt_y = 40, -80
	for point in Polys:
		lb_x = min(point.x, lb_x)
		lb_y = min(point.y, lb_y)
		rt_x = max(point.x, rt_x)
		rt_y = max(point.y, rt_y)
	print lb_x, lb_y, rt_x, rt_y
	leftBottom = Point(lb_x,lb_y)
	rightTop = Point(rt_x, rt_y)
	result = intersection(idx, leftBottom, rightTop)
	print j, result

