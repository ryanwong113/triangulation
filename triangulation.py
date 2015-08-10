import itertools
import random
import matplotlib.pyplot as pyplot
import math
from matplotlib.collections import PolyCollection
from operator import attrgetter


# Inner point class
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __cmp__(self, other):
		return self.x.__cmp__(other.x) and self.y.__cmp__(other.y)

	def __repr__(self):
		return 'Point(x=%d, y=%d)' % (self.x, self.y)

# Inner line class
class Line:
	def __init__(self, point_a, point_b):
		self.point_a = point_a
		self.point_b = point_b

	def __cmp__(self, other):
		return self.point_a.__cmp__(other.point_a) and self.point_b.__cmp__(other.point_b)

	def __repr__(self):
		return 'Line(%s-%s)' % (self.point_a, self.point_b)

# Inner segment class
class Segment:
	def __init__(self, points, lines):
		self.points = points
		self.lines = lines
		self.lowest_point = min(points, key=attrgetter('y'))
		self.size = len(points)

	def __repr__(self):
		return 'Segment %d' % (self.size)


# Main program
# Key function for sorting the point
def get_point_order_key(point):
	return (point.x, point.y)

# Split the points into segments
def split_points(points):
	if (len(points) <= 3):
		return Segment(points, [Line(combination[0], combination[1]) for combination in itertools.combinations(points, 2)])
	else:
		split_index = int(math.ceil(len(points)/2.0))
		return [split_points(points[:split_index])] + [split_points(points[split_index:len(points)])]

# Merge the segments
def merge_segments(segments):
	for segment in segments:
		if type(segment) is list:
			merge_segments(segment)
		else:
			# Merge 2 segments together
			points = []
			lines = []
			segment_left = segment[0]
			segment_right = segemnt[1]
			segment_left_lowest = segment_left.lowest_point
			segment_right_lowest = segment_right.lowest_point

			# Remove the lowest points from left and right segments
			segment_left.remove(segment_left_lowest)
			segment_right.remove(segment_right_lowest)

			# Base line
			base_line = Line(segemnt_left_lowest, segemnt_right_lowest)
			lines.append(base_line)

			# Check right segment
			for i in range(len(segment_right.points)-1)
				current_candidate = segment_right.points[i]
				next_candidate = segment_right.points[i+1]

				# Check current candidate is less than 180 degree


			


			# Check left segment
			for point in segment_left.points:
				
			# New segment
			points.extend(segment_left.points).extend(segment_right.points)
			lines.extend(segment_left.lines).extend(segment_right.lines)
			Segment(points, lines)
			break

			


# Initialisation
def init():
	range_min = 1
	range_max = 10
	num_of_points = 10
	points = [[Point(random.randint(range_min, range_max), random.randint(range_min, range_max)) for i in range(0, num_of_points)]]
	points[0].sort(key=get_point_order_key)
	point_segments = split_points(points[0])
	
	# print point_segments
	merge_segments(point_segments)

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

	pyplot.plot(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
	pyplot.show() 

#plot(compute(init()))
init()
