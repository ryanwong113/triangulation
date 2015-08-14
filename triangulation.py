import itertools
import random
# import matplotlib.pyplot as pyplot
import math
# from matplotlib.collections import PolyCollection
import operator

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

	def __eq__(self, other):
		return ((self.point_a == other.point_a) and (self.point_b == other.point_b)) or ((self.point_a == other.point_b) and (self.point_b == other.point_a))

	def __cmp__(self, other):
		return (self.point_a.__cmp__(other.point_a) and self.point_b.__cmp__(other.point_b)) or (self.point_a.__cmp__(other.point_b) and self.point_b.__cmp__(other.point_a))

	def __repr__(self):
		return 'Line(%s-%s)' % (self.point_a, self.point_b)

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

# See whether other_points is contained in the triangle formed by point_a, point_b, point_c
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

	det = a*(e*i-c*f)-b*(d*i-f*g)+c*(d*h-e*g)
	
	# If det > 0, other_point is in circumcircle. So return false
	return (det <= 0)


# Recursive function for generating new segment by merging two segments together
def generate_new_segment():
	# Left and right base line points
	left_base_line_point = base_line.point_a
	right_base_line_point = base_line.point_b

	# Check right segment
	# Build a map of points to angle to the lowest_point
	angle_map = {}
	for point in segment_right.points:
		vertical_distance = point.y - right_base_line_point.y
		horizontal_distance = right_base_line_point.x - point.x

		# Use 4 quadrants to find the angle
		if vertical_distance == 0:
			if horizontal_distance > 0:
				angle = 0
			else:
				angle = math.pi
			angle_map[point] = angle
		elif horizontal_distance == 0:
			if vertical_distance > 0:
				angle = math.pi/2
				angle_map[point] = angle
		elif vertical_distance > 0: 
			# In first quadrant
			if horizontal_distance > 0:
				angle = math.atan(float(vertical_distance)/float(horizontal_distance))
			# In second quadrant
			else:
				angle = math.pi - math.atan(float(vertical_distance)/float(-horizontal_distance))
			angle_map[point] = angle

	# There are no right candidates. Go check left segment.
	if len(angle_map) == 0:
		continue
	else:
		confirmed_right_candidate = None
		candidates = sorted(angle_map.items(), key=operator.itemgetter(1))
		if (len(candidates) == 1):
			confirmed_right_candidate = candidates[0][0]
		else:
			for i in range(len(candidates)-1):
				current_candidate = candidates[i][0]
				next_candidate = candidates[i+1][0]

				# If next_candidate is in circumcircle
				if (in_circumcircle(left_base_line_point, right_base_line_point, current_candidate, next_candidate)):
					# current_candidate is not the confirmed right segment candidate
					lines.remove(Line(right_base_line_point, current_candidate))
				else:
					# current_candidate is the confirmed right segment candidate
					confirmed_right_candidate = current_candidate
					break

	# Check left segment
	angle_map = {}
	for point in segment_left.points:
		vertical_distance = point.y - left_base_line_point.y
		horizontal_distance = point.x - left_base_line_point.x

		# Use 4 quadrants to find the angle
		if vertical_distance == 0:
			if horizontal_distance > 0:
				angle = 0
			else:
				angle = math.pi
			angle_map[point] = angle
		elif horizontal_distance == 0:
			if vertical_distance > 0:
				angle = math.pi/2
				angle_map[point] = angle
		elif vertical_distance > 0: 
			# In first quadrant
			if horizontal_distance > 0:
				angle = math.atan(float(vertical_distance)/float(horizontal_distance))
			# In second quadrant
			else:
				angle = math.pi - math.atan(float(vertical_distance)/float(-horizontal_distance))
			angle_map[point] = angle

	# There are no left candidates.
	if len(angle_map) == 0:
		continue
	else:
		confirmed_left_candidate = None
		candidates = sorted(angle_map.items(), key=operator.itemgetter(1))
		if (len(candidates) == 1):
			confirmed_left_candidate = candidates[0][0]
		else:
			for i in range(len(candidates)-1):
				current_candidate = candidates[i][0]
				next_candidate = candidates[i+1][0]

				# If next_candidate is in circumcircle
				if (in_circumcircle(left_base_line_point, right_base_line_point, current_candidate, next_candidate)):
					# current_candidate is not the confirmed right segment candidate
					lines.remove(Line(left_base_line_point, current_candidate))
				else:
					# current_candidate is the confirmed left segment candidate
					confirmed_left_candidate = current_candidate
					break
		
	# Finished merging segment
	if (confirmed_right_candidate is None) and (confirmed_left_candidate is None):
		# Create and return a new merged segment
		return Segment(points, lines)
	elif (confirmed_right_candidate is not None) and (confirmed_left_candidate is None):
		new_line = Line(confirmed_right_candidate, left_base_line_point)
		lines.append(new_line)
	elif (confirmed_right_candidate is None) and (confirmed_left_candidate is not None):
		new_line = Line(confirmed_left_candidate, right_base_line_point)
		lines.append(new_line)
	else:
		if in_circumcircle(left_base_line_point, right_base_line_point, confirmed_left_candidate, confirmed_right_candidate):
			new_line = Line(confirmed_right_candidate, left_base_line_point)
		else:
			new_line = Line(confirmed_left_candidate, right_base_line_point)
		lines.append(new_line)



# Merge the segments
def merge_segments(segments):
	for segment in segments:
		if type(segment) is list:
			merge_segments(segment)
		else:
			# Merge 2 segments together
			points = []
			lines = []

			segment_left = segments[0]
			segment_right = segments[1]
			segment_left_lowest = segment_left.lowest_point
			segment_right_lowest = segment_right.lowest_point

			points.extend(segment_left.points)
			points.extend(segment_right.points)
			lines.extend(segment_left.lines)
			lines.extend(segment_right.lines)

			# Remove the lowest points from left and right segments
			segment_left.points.remove(segment_left_lowest)
			segment_right.points.remove(segment_right_lowest)

			# Base line
			base_line = Line(segment_left_lowest, segment_right_lowest)
			lines.append(base_line)

			############################
			### Start recursive here ###
			############################

			


			


# Initialisation
def init():
	range_min = 1
	range_max = 10
	num_of_points = 50
	points = [[]]
	for i in range(0, num_of_points):
		new_point = Point(random.randint(range_min, range_max), random.randint(range_min, range_max))
		if new_point not in points[0]:
			points[0].append(new_point)
	points[0].sort(key=get_point_order_key)
	point_segments = split_points(points[0])
	merge_segments(point_segments)

	return points


# def plot(triangles):
# 	for triangle in triangles:
# 		points = [[triangle[0].x, triangle[0].y], [triangle[1].x, triangle[1].y], [triangle[2].x, triangle[2].y]]
# 		shape = pyplot.Polygon(points, fill=None, edgecolor='r')
# 		pyplot.gca().add_patch(shape)

# 	pyplot.plot(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
# 	pyplot.show() 

#plot(compute(init()))
init()
