import json
from spatial import *
import csv
import time
import math

with open('ny.geojson') as f:
    data = json.load(f)

polygon_list = []
lis_dic = data['features']
for dic in lis_dic:
	dic_dic = dic['geometry']
	polygon_list.append(dic_dic["coordinates"])
f.close()

Polygon_lis = []
for polygons in polygon_list:
	Points = []
	for polygon in polygons:
		for points in polygon:
			if len(points)==2:
				Points.append(Point(points[1], points[0]))
			else:
				for point in points:
					Points.append(Point(point[1], point[0]))
	Polygon_lis.append(Points)

result = []
with open('result.txt') as r:
	lines = r.readlines()
	i = float(0)
	
	for line in lines:
		line = line.rstrip().split(" ")
		num = float(line[0])
		if num == i:
			i += 1
			result.append(int(line[1]))
r.close()
print result
draw_color = []
colors = [1,2,3,4,5,6,7,8,9]

log_result = []
for key in result:
	log_result.append(math.log(key))
mini = min(log_result)
maxi = max(log_result)
stage = (maxi-mini) / (len(colors)-1)
for key in log_result:
	index = int((key-mini) / stage)
	draw_color.append(colors[index])

print draw_color
print len(set(draw_color))

with open('ny.geojson') as f:
    data = json.load(f)

lis_dic = data['features']
for i, dic in enumerate(lis_dic):
	dic['properties']['color'] = draw_color[i]
import json
with open('ny_with_color_jun_2015_green.geojson', 'w') as outfile:
    json.dump(data, outfile)
outfile.close()

f.close()









		
