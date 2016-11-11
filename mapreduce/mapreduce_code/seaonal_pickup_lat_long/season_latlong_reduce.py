#!/usr/bin/python
'''lat long in different season'''
import sys

current_key = None

for line in sys.stdin:
	if len(line.strip().split('\t'))==2:
		old_key, value = line.strip().split('\t')
		lat, lon, boro, cnt = value.split(',')

		# print seasonal latlong
		if old_key[:7] in ['2014-06','2014-07','2014-08']:
			key = 'summer'
		# if old_key[:7] in ['2014-09','2014-10','2014-11']:
		# 	key = 'fall'
		# if old_key[:7] in ['2014-12','2015-01','2015-02']:
		# 	key = 'winter'
		# if old_key[:7] in ['2015-03','2015-04','2015-06']:
		# 	key = 'spring'

			print lat, lon