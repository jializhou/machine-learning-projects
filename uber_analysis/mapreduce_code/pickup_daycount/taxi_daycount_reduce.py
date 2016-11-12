#!/usr/bin/python
'''number conut per day'''
import sys

current_key = None
current_sum= 0

for line in sys.stdin:
	# print len(line.strip().split('\t'))
	if len(line.strip().split('\t')) == 2:
		key, value = line.strip().split('\t')
		lat, lon, boro, cnt  = value.split(',')

		if key == current_key:
			current_sum += int(cnt)

		else: 
			if current_key: 
				print '%s\t%s' %(current_key, current_sum) # print the previous key-value pair
			current_key = key
			current_sum = int(cnt)
	else:
		continue
	#print the last key-value pair:
print '%s\t%s' %(current_key, current_sum)
