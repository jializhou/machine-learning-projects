### color_map.py
from lxml import etree as ET
import os
# Read in count
def get_count_by_name_year(path, name, year):
    count = {}
    for file in os.listdir(path):
        if file.endswith(".TXT"):           
            file = os.path.join(path, file)
            reader = open(file, 'r').readlines()
            for row in reader:
                row = row.rstrip().split(',')
                if row[2] == year and row[3] == name:
                    full_fips = row[0]
                    rate = int( row[4] )
                    count[full_fips] = rate
    return count

def get_count_by_name_gender(path, name, gender):
    count = {}
    for file in os.listdir(path):
        if file.endswith(".TXT"):           
            file = os.path.join(path, file)
            reader = open(file, 'r').readlines()
            for row in reader:
                row = row.rstrip().split(',')
                if row[1] == gender and row[3] == name:
                    full_fips = row[0]
                    rate = int( row[4] )
                    if full_fips not in count:
                        count[full_fips] = 0
                    count[full_fips] += rate / float(2014-1910+1)
    return count

def get_count_by_name_gender_year(path, name, gender, year):
    count = {}
    for file in os.listdir(path):
        if file.endswith(".TXT"):           
            file = os.path.join(path, file)
            reader = open(file, 'r').readlines()
            for row in reader:
                row = row.rstrip().split(',')
                if row[1] == gender and row[2] == year and row[3] == name:
                    full_fips = row[0]
                    rate = int( row[4] )
                    count[full_fips] = rate 
    return count
path = "namesbystate" 
count = get_count_by_name_year(path, 'Oliver', '2013')
# count = get_count_by_name_gender(path, 'James', 'M')
# count = get_count_by_name_gender_year(path, 'Maxie', 'F', '1945')
# for key, value in count.items():
#     print key, value
# Load the SVG map
svg = open('states.svg', 'r').read()


# Map colors
# colors = ["#ff74c4", "#ff39aa", "#fe0091", "#d6007b", "#9c0059", '#740042']
# colors = ['#81ffb7','#74ffaf','#5ccc8c','#459969','#2e6646','#173323']
colors = ['#ff9da5','#ff747f','#cc5c65','#99454c','#662e32','#331719']
# State style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
 
# Color the states based on count
tree = ET.parse('states.svg')
root = tree.getroot()
for child in root:
    flag = False
    if 'path' in child.tag and 'id' in child.attrib:
        p = child.attrib
        flag = True
    elif 'g' in child.tag:
        for next_child in child:
            if 'path' in next_child.tag and 'id' in next_child.attrib:
                p = next_child.attrib
                flag = True
    if flag:
        rate = 0
        print p['id']
        if p['id'] in count:
            rate = count[p['id']]
             
        if rate > 400:
            color_class = 5
        elif rate > 200:
            color_class = 4
        elif rate > 100:
            color_class = 3
        elif rate > 50:
            color_class = 2
        elif rate > 10:
            color_class = 1
        else:
            color_class = 0

     
        # print color_class
        color = colors[color_class]
        p['style'] = path_style + color

tree.write('Oliver_2013.svg')
