import copy
import itertools
import math
import operator
import random
from pyx import *
# import matplotlib.pyplot as pyplot
# from matplotlib.collections import PolyCollection

# Inner point class
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)

	def __cmp__(self, other):
		return self.x.__cmp__(other.x) and self.y.__cmp__(other.y)

	def __hash__(self):
		return hash(self.x) * hash(self.y)

	def __repr__(self):
		return 'Point(x=%d, y=%d)' % (self.x, self.y)

# Inner line class
class Line:
	def __init__(self, point_a, point_b):
		self.point_a = point_a
		self.point_b = point_b
		self.distance = math.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

	def __eq__(self, other):
		return ((self.point_a == other.point_a) and (self.point_b == other.point_b)) or ((self.point_a == other.point_b) and (self.point_b == other.point_a))

	def __cmp__(self, other):
		return (self.point_a.__cmp__(other.point_a) and self.point_b.__cmp__(other.point_b)) or (self.point_a.__cmp__(other.point_b) and self.point_b.__cmp__(other.point_a))

	def __repr__(self):
		return 'Line(%s, %s)' % (self.point_a, self.point_b)

# Inner segment class
class Segment:
	def __init__(self, points, lines):
		self.points = points
		self.lines = lines
		self.lowest_point = min(points, key=operator.attrgetter('y'))
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

# See whether other_points is contained in the circumcircle formed by point_a, point_b, point_c
def in_circumcircle(point_a, point_b, point_c, other_point):
	a = point_a.x - other_point.x
	b = point_a.y - other_point.y
	c = (point_a.x**2 - other_point.x**2) + (point_a.y**2 - other_point.y**2)
	d = point_b.x - other_point.x
	e = point_b.y - other_point.y
	f = (point_b.x**2 - other_point.x**2) + (point_b.y**2 - other_point.y**2)
	g = point_c.x - other_point.x
	h = point_c.y - other_point.y
	i = (point_c.x**2 - other_point.x**2) + (point_c.y**2 - other_point.y**2)

	det = (a * ((e * i) - (f * h))) - (b * ((d * i) - (f * g))) + (c * ((d * h) - (e * g)))
	
	# If det > 0, other_point is in circumcircle. So return false
	return (det > 0)


# Recursive function for generating lines connecting two segments
def generate_lines_connecting_two_segments(base_line, lines, full_segment_left, full_segment_right):
	# Left and right base line points
	left_base_line_point = base_line.point_a
	right_base_line_point = base_line.point_b

	# Remove the base line points from left and right segments
	segment_left = copy.deepcopy(full_segment_left)
	segment_right = copy.deepcopy(full_segment_right)
	segment_left.points.remove(left_base_line_point)
	segment_right.points.remove(right_base_line_point)

	# Check right segment
	# Build a map of points to angle to the lowest_point
	base_line_vector = Point(left_base_line_point.x - right_base_line_point.x, left_base_line_point.y - right_base_line_point.y)
	angle_map = {}
	for point in segment_right.points:
		right_to_point_vector = Point(point.x - right_base_line_point.x, point.y - right_base_line_point.y)
		angle = math.atan2((right_to_point_vector.x * base_line_vector.y) - (base_line_vector.x * right_to_point_vector.y), (base_line_vector.x * right_to_point_vector.x) + (base_line_vector.y * right_to_point_vector.y))

		if angle >= 0 and angle < math.pi:
			angle_map[point] = angle

	# Check whether there are any candidates in the right segment
	candidates = sorted(angle_map.items(), key=operator.itemgetter(1))
	confirmed_right_candidate = None
	if len(candidates) == 1:
		confirmed_right_candidate = candidates[0][0]
	elif len(candidates) > 1:
		for i in range(len(candidates)-1):
			current_candidate = candidates[i][0]
			next_candidate = candidates[i+1][0]

			# If next_candidate is in circumcircle. Note: the order of first 3 arguments must be counter-clockwise
			if (in_circumcircle(left_base_line_point, right_base_line_point, current_candidate, next_candidate)):
				# current_candidate is not the confirmed right segment candidate
				line_to_be_removed = Line(current_candidate, right_base_line_point)
				if line_to_be_removed in lines:
					lines.remove(line_to_be_removed)
			else:
				# current_candidate is the confirmed right segment candidate
				if confirmed_right_candidate is None:
					confirmed_right_candidate = current_candidate

	# Check left segment
	# Build a map of points to angle to the lowest_point
	base_line_vector = Point(right_base_line_point.x - left_base_line_point.x, right_base_line_point.y - left_base_line_point.y)
	angle_map = {}
	for point in segment_left.points:
		left_to_point_vector = Point(point.x - left_base_line_point.x, point.y - left_base_line_point.y)

		angle = math.atan2((left_to_point_vector.x * base_line_vector.y) - (base_line_vector.x * left_to_point_vector.y), (base_line_vector.x * left_to_point_vector.x) + (base_line_vector.y * left_to_point_vector.y))

		if angle > -math.pi and angle <= 0:
			angle_map[point] = -angle

	# Check whether there are any candidates in the left segment
	candidates = sorted(angle_map.items(), key=operator.itemgetter(1))
	confirmed_left_candidate = None
	if len(candidates) == 1:
		confirmed_left_candidate = candidates[0][0]
	elif len(candidates) > 1:
		for i in range(len(candidates)-1):
			current_candidate = candidates[i][0]
			next_candidate = candidates[i+1][0]
			# If next_candidate is in circumcircle. Note: the order of first 3 arguments must be counter-clockwise
			if (in_circumcircle(left_base_line_point, right_base_line_point, current_candidate, next_candidate)):
				# current_candidate is not the confirmed left segment candidate
				line_to_be_removed = Line(left_base_line_point, current_candidate)
				if line_to_be_removed in lines:
					lines.remove(line_to_be_removed)
			else:
				# current_candidate is the confirmed left segment candidate
				if confirmed_left_candidate is None:
					confirmed_left_candidate = current_candidate
	
	# Try adding a new line to connect two segments
	# Create and return a new merged segment
	if (confirmed_right_candidate is None) and (confirmed_left_candidate is None):
		return lines
	elif (confirmed_right_candidate is not None) and (confirmed_left_candidate is None):
		new_line = Line(left_base_line_point, confirmed_right_candidate)
		lines.append(new_line)
	elif (confirmed_right_candidate is None) and (confirmed_left_candidate is not None):
		new_line = Line(confirmed_left_candidate, right_base_line_point)
		lines.append(new_line)
	else:
		if in_circumcircle(left_base_line_point, right_base_line_point, confirmed_left_candidate, confirmed_right_candidate):
			new_line = Line(left_base_line_point, confirmed_right_candidate)
		else:
			new_line = Line(confirmed_left_candidate, right_base_line_point)
	lines.append(new_line)

	return generate_lines_connecting_two_segments(new_line, lines, full_segment_left, full_segment_right)


# Merge the segments
def merge_segments(segments):
	points = []
	lines_connecting_segments = []

	if type(segments) is list:
		for segment in segments:
			if type(segment) is list:
				return merge_segments([merge_segments(segments[0]), merge_segments(segments[1])])
			else:
				# Merge 2 segments together
				segment_left = segments[0]
				segment_right = segments[1]
				segment_left_lowest = segment_left.lowest_point
				segment_right_lowest = segment_right.lowest_point

				# Initiate the new segment points and lines
				points.extend(segment_left.points + segment_right.points)
				lines = segment_left.lines + segment_right.lines

				# Starting base line
				base_line = Line(segment_left_lowest, segment_right_lowest)
				lines.append(base_line)

				# Generate the lines connecting two segments
				lines_connecting_segments.extend(generate_lines_connecting_two_segments(base_line, lines, segment_left, segment_right))

				return Segment(points, lines_connecting_segments)

	return segments




# def plot(triangles):
# 	for triangle in triangles:
# 		points = [[triangle[0].x, triangle[0].y], [triangle[1].x, triangle[1].y], [triangle[2].x, triangle[2].y]]
# 		shape = pyplot.Polygon(points, fill=None, edgecolor='r')
# 		pyplot.gca().add_patch(shape)

# 	pyplot.plot(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
# 	pyplot.show() 
	

#plot(compute(init()))








