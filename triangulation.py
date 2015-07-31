import itertools
import random
import matplotlib.pyplot as pyplot
from matplotlib.collections import PolyCollection


# Innter point class
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return 'Point[x=%d, y=%d]' % (self.x, self.y)

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)

# Main program
# Initialisation
def init():
	points = []
	range_min = 1
	range_max = 50
	num_of_points = 10
	for i in range(0, num_of_points):
		rand_x = random.randint(range_min, range_max)
		rand_y = random.randint(range_min, range_max)
		point = Point(rand_x, rand_y)
		points.append(point)

	return points

def compute(all_points):
	results = []
	combinations = itertools.combinations(all_points, 3)
	for combination in combinations:
		other_points = all_points[:]
		point_a = combination[0]
		point_b = combination[1]
		point_c = combination[2]

		other_points.remove(point_a)
		other_points.remove(point_b)
		other_points.remove(point_c)

		if form_triangle(point_a, point_b, point_c, other_points):
			results.append(combination)

	return results


# Test whether the given three points form a triangle or not
def form_triangle(point1, point2, point3, other_points):
	for other_point in other_points:
		a = point1.x - other_point.x
		b = point1.y - other_point.y
		c = (point1.x**2 - other_point.x**2) + (point1.y**2 - other_point.y**2)
		d = point2.x - other_point.x
		e = point2.y - other_point.y
		f = (point2.x**2 - other_point.x**2) + (point2.y**2 - other_point.y**2)
		g = point3.x - other_point.x
		h = point3.y - other_point.y
		i = (point3.x**2 - other_point.x**2) + (point3.y**2 - other_point.y**2)

		det = a*(e*i-c*f)-b*(d*i-f*g)+c*(d*h-e*g)
		
		# If det > 0, other_point is in circumcircle. So return false
		if det > 0:
			return False
	return True

def plot(triangles):
	for triangle in triangles:
		points = [[triangle[0].x, triangle[0].y], [triangle[1].x, triangle[1].y], [triangle[2].x, triangle[2].y]]
		shape = pyplot.Polygon(points, fill=None, edgecolor='r')
		pyplot.gca().add_patch(shape)

	pyplot.plot()
	pyplot.show() 

plot(compute(init()))


