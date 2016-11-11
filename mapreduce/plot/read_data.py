import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
from pysal.esda.mapclassify import Natural_Breaks as nb
from descartes import PolygonPatch
import fiona
from itertools import chain
import pysal.esda.mapclassify as mapclassify
 
r = fiona.open('ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp')

bds = r.bounds

#define a variable called extra which we will use for padding the map when we display it (in this case I've selected a 10% pad)
extra = 0.1

#define the lower left hand boundary (longitude, latitude)
ll = (bds[0], bds[1])

#define the upper right hand boundary (longitude, latitude)
ur = (bds[2], bds[3])

#concatenate the lower left and upper right into a variable called coordinates
coords = list(chain(ll, ur))

#define variables for the width and the height of the map
w, h = coords[2] - coords[0], coords[3] - coords[1]


m = Basemap(
    #set projection to 'tmerc' which is apparently less distorting when close-in
    projection='tmerc',

    #set longitude as average of lower, upper longitude bounds
    lon_0 = np.average([bds[0],bds[2]]),

    #set latitude as average of lower,upper latitude bounds
    lat_0 = np.average([bds[1],bds[3]]),

    ellps = 'WGS84',
    
    #set the map boundaries. Note that we use the extra variable to provide a 10% buffer around the map
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,

    #provide latitude of 'true scale.' Not sure what this means, I would check the Basemap API if you are a GIS guru
    lat_ts=0,

    #resolution of boundary database to use. Can be c (crude), l (low), i (intermediate), h (high), f (full) or None.
    resolution='i',
    
    #don't show the axis ticks automatically
    suppress_ticks=True)

m.readshapefile(
    #provide the path to the shapefile, but leave off the .shp extension
    'ZillowNeighborhoods-NY/ZillowNeighborhoods-NY',

    #name your map something useful (I named this 'srilanka')
    'NY',

    #set the default shape boundary coloring (default is black) and the zorder (layer order)
    color='none',
    zorder=2)


m.srilanka_info[0]

