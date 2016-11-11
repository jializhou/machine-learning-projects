#!/usr/bin/python
'''
Input:  must be the output from the first-stage cleaned format

Output: Number count per month in bk or any one of the counties in NYC 
by changing the if-condition "if boro == 'county_name'.

"'''
import sys

current_key = None
current_sum= 0

for line in sys.stdin:
	if len(line.strip().split('\t'))==2:
		old_key, value = line.strip().split('\t')
		lat, lon, boro, cnt = value.split(',')
		key = old_key[:7]
	else:
		continue

	if key == current_key:
		if boro == 'Brooklyn': # look for pickups in only Brooklyn
		# if boro == 'Bronx': # look for pickups in only Bronx
			current_sum += int(cnt)

	else: 
		if current_key: 
			print '%s\t%s' %(current_key, current_sum) # print the previous key-value pair
		current_key = key
		current_sum = int(cnt)

#print the last key-value pair:
print '%s\t%s' %(current_key, current_sum)