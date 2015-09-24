import copy
import itertools
import math
import operator
import random

from pyx import *
import matplotlib.pyplot as pyplot

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
		self.size = len(points)
		self.lowest_point = min(points, key=operator.attrgetter('y'))

	def __repr__(self):
		return 'Segment size: %s' % (self.size)


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

# Recursive function for generating lines connecting two segments (upwards)
def generate_lines_connecting_two_segments_upwards(base_line, lines, full_segment_left, full_segment_right):
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
	num_of_candidates = len(candidates)
	for i in range(num_of_candidates):
		current_candidate = candidates[i][0]
		if (i + 1 < num_of_candidates):
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
		else:
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
	num_of_candidates = len(candidates)
	for i in range(num_of_candidates):
		current_candidate = candidates[i][0]
		if (i + 1 < num_of_candidates):
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
		else:
			if confirmed_left_candidate is None:
				confirmed_left_candidate = current_candidate
	
	# Try adding a new line to connect two segments
	# Return the lines connecting the segments. Otherwise append the new line.
	if (confirmed_right_candidate is None) and (confirmed_left_candidate is None):
		return lines
	elif (confirmed_right_candidate is not None) and (confirmed_left_candidate is None):
		new_line = Line(left_base_line_point, confirmed_right_candidate)
	elif (confirmed_right_candidate is None) and (confirmed_left_candidate is not None):
		new_line = Line(confirmed_left_candidate, right_base_line_point)
	else:
		if in_circumcircle(left_base_line_point, right_base_line_point, confirmed_left_candidate, confirmed_right_candidate):
			new_line = Line(left_base_line_point, confirmed_right_candidate)
		else:
			new_line = Line(confirmed_left_candidate, right_base_line_point)
	lines.append(new_line)

	return generate_lines_connecting_two_segments_upwards(new_line, lines, full_segment_left, full_segment_right)

# Recursive function for generating lines connecting two segments (downwards)
def generate_lines_connecting_two_segments_downwards(base_line, lines, full_segment_left, full_segment_right):
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
	num_of_candidates = len(candidates)
	for i in range(num_of_candidates):
		current_candidate = candidates[i][0]
		if (i + 1 < num_of_candidates):
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
		else:
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
	num_of_candidates = len(candidates)
	for i in range(num_of_candidates):
		current_candidate = candidates[i][0]
		if (i + 1 < num_of_candidates):
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
		else:
			if confirmed_left_candidate is None:
				confirmed_left_candidate = current_candidate
	
	# Try adding a new line to connect two segments
	# Return the lines connecting the segments. Otherwise append the new line.
	if (confirmed_right_candidate is None) and (confirmed_left_candidate is None):
		return lines
	elif (confirmed_right_candidate is not None) and (confirmed_left_candidate is None):
		new_line = Line(left_base_line_point, confirmed_right_candidate)
	elif (confirmed_right_candidate is None) and (confirmed_left_candidate is not None):
		new_line = Line(confirmed_left_candidate, right_base_line_point)
	else:
		if in_circumcircle(left_base_line_point, right_base_line_point, confirmed_left_candidate, confirmed_right_candidate):
			new_line = Line(left_base_line_point, confirmed_right_candidate)
		else:
			new_line = Line(confirmed_left_candidate, right_base_line_point)
	lines.append(new_line)

	return generate_lines_connecting_two_segments_downwards(new_line, lines, full_segment_left, full_segment_right)

def find_initial_base_line(segment_left, segment_right):
	base_point_a = segment_left.lowest_point
	base_point_b = segment_right.lowest_point

	# Remove any intersecting lines in the left segment
	removed_lines = []
	for line in segment_left.lines:
		if lines_intersect(base_point_a, base_point_b, line.point_a, line.point_b):
			removed_lines.append(line)

	for removed_line in removed_lines:
		segment_left.lines.remove(removed_line)
	
	# Remove any intersecting lines in the right segment
	removed_lines = []
	for line in segment_right.lines:
		if lines_intersect(base_point_a, base_point_b, line.point_a, line.point_b):
			removed_lines.append(line)

	for removed_line in removed_lines:
		segment_right.lines.remove(removed_line)

	return segment_left, segment_right, Line(base_point_a, base_point_b)

# Given four points, check whether the lines intersect (line_1 = point_a and point_b) (line_2 = point_c and point_d)
def lines_intersect(point_a, point_b, point_c, point_d):
	subtract_points = Point(point_c.x - point_a.x, point_c.y - point_a.y)

	r = Point(point_b.x - point_a.x, point_b.y - point_a.y)
	s = Point(point_d.x - point_c.x, point_d.y - point_c.y)

	u_numerator = (subtract_points.x * r.y) - (subtract_points.y * r.x)
	denominator = (r.x * s.y) - (r.y * s.x)

	# The lines are collinear, so intersect if they have any overlap
	if u_numerator == 0 and denominator == 0:	
		return ((point_c.x - point_a.x < 0) != (point_c.x - point_b.x < 0) != (point_d.x - point_a.x < 0) != (point_d.x - point_b.x < 0)) or \
		((point_c.y - point_a.y < 0) != (point_c.y - point_b.y < 0) != (point_d.y - point_a.y < 0) != (point_d.y - point_b.y < 0))

	# The lines are parallel
	if denominator == 0:
		return False

	u = u_numerator / float(denominator)
	t = (subtract_points.x * s.y - subtract_points.y * s.x) / float(denominator)

	return (t > 0.0) and (t < 1.0) and (u > 0.0) and (u < 1.0)

# Merge the segments
def merge_segments(segments):
	if type(segments) is list:
		segment_left = segments[0]
		segment_right = segments[1]
		if type(segments[0]) is list:
			return merge_segments([merge_segments(segment_left), merge_segments(segment_right)])
		else:
			# Initiate the new segment points and lines
			points = segment_left.points + segment_right.points

			# Find the initial base line
			segment_left, segment_right, base_line = find_initial_base_line(segment_left, segment_right)
			lines = segment_left.lines + segment_right.lines + [base_line]

			# Generate the lines connecting two segments
			lines_connecting_segments = generate_lines_connecting_two_segments_upwards(base_line, lines, segment_left, segment_right)

			# new_segment = Segment(points, lines_connecting_segments)
			# plot_matplotlib(new_segment)

			return Segment(points, lines_connecting_segments)

	return segments

# Draw the image using pyx
def plot_pyx(segment):
	c = canvas.canvas()
	lines = segment.lines
	for line in lines:
		c.stroke(path.line(line.point_a.x, line.point_a.y, line.point_b.x, line.point_b.y))
	c.writeEPSfile("path")

# Draw the image using matplotlib
def plot_matplotlib(segment):
	lines = segment.lines
	for line in lines:
		point_a = line.point_a
		point_b = line.point_b
		pyplot.plot([point_a.x, point_b.x], [point_a.y, point_b.y])

	pyplot.show() 








