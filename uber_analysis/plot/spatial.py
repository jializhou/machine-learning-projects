import time
from rtree import index

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Polygon:
	def __init__(self,points):
		self.points = points
		self.nvert = len(points)

	def contains(self,pt):
		firstX = self.points[0].x
		firstY = self.points[0].y
		testx = pt.x
		testy = pt.y
		c = False
		j = 0
		i = 1
		nvert = self.nvert
		while (i < nvert) :
			vi = self.points[i]
			vj = self.points[j]
			
			if(((vi.y > testy) != (vj.y > testy)) and (testx < (vj.x - vi.x) * (testy - vi.y) / (vj.y - vi.y) + vi.x)):
				c = not(c)

			if(vi.x == firstX and vi.y == firstY):
				i = i + 1
				if (i < nvert):
					vi = self.points[i];
					firstX = vi.x;
					firstY = vi.y;
			j = i
			i = i + 1
		return c



def simplePolygonTest(poly, pt):
	# print("Point in polygon test")
	# Create a simple polygon
	# poly = Polygon([Point(0.0, 0.0),Point(0.0, 4.0),Point(3.0, 4.0),Point(3.0, 0.0)])

	# Create two points
	# pt1 = Point(1,1)
	# pt2 = Point(4,1)

	# Test if the polygon contains the two points
	if poly.contains(pt):
		# print("Point ("+ str(pt.x)+", "+str(pt.y)+") is within the polygon")
		return True
	else:
		return False
		# print("Point ("+ str(pt.x)+", "+str(pt.y)+") is outside the polygon")



def simpleRTree_insert(pts):
	# print("R-tree test")
	idx = index.Index()

	for i, pt in enumerate(pts):
		# Insert the points into the R-tree index
		idx.insert(i+1,(pt.x,pt.y,pt.x,pt.y))
	return idx
	
def intersection(idx, leftBottom, rightTop):
	results = list(idx.intersection((leftBottom.x,leftBottom.y,rightTop.x,rightTop.y)))
	# print "time to calculate points using R-tree:", time.time() - t1
	# print("Query result:")
	return len(results)

# simplePolygonTest()
# simpleRTree()
