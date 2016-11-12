import numpy as np
import re
import itertools
from collections import Counter
import os

w = open('./fastText/train.txt','w')
path1, path2 = "./train/pos","./train/neg"

def write(path1, path2, w):    
	for file in os.listdir(path1):
	    if file.endswith(".txt"):
	    	# print file
	        w.write(open(path1+'/'+file, "r").readlines()[0]+' __label__1 \n')
	for file in os.listdir(path2):
	    if file.endswith(".txt"):
	        w.write(open(path2+'/'+file, "r").readlines()[0]+' __label__0 \n')
	w.close()

write(path1, path2, w)
r = open('./fastText/train.txt','r')
print len(r.readlines())
