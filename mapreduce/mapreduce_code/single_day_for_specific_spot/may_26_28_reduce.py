#!/usr/bin/python
'''output points in any demanded small grid (e.g.lat ~[40.74, 40.5], long~ [-73.98, -73.99]), 
a focused spot around Empire State building on a given date (e.g. 2014-05-26)'''
import sys

current_key = None

for line in sys.stdin:
	if len(line.strip().split('\t'))==2:
		old_key, value = line.strip().split('\t')
		lat, lon, boro, cnt = value.split(',')
		key = old_key[:10]
		
		if key == '2014-05-26':
		# if key =='2014-05-28':
			if (abs(lat - 40.74) <= 0.01) and (abs(lon +73.99) <= 0.01):
				print lat, lon 