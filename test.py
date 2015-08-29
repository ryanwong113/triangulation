from triangulation import *

def test_in_circumcirle():
	point_a = Point(10, 0)
	point_b = Point(10, 2)
	point_c = Point(8, 4)
	other_point = Point(6, 6)

	if in_circumcircle(point_a, point_b, point_c, other_point):
		print 'Yes in circumcirle'
	else:
		print 'No'

def test_case():
	# points = [[Point(2, 6), Point(6, 6), Point(10, 6), Point(2, 4), Point(8, 4), Point(0, 2), Point(4, 2), Point(10, 2), Point(2, 0), Point(10, 0)]]
	# points = [[Point(6, 6), Point(10, 6), Point(8, 4), Point(10, 2), Point(10, 0)]]
	# points = [[Point(2, 6), Point(2, 4), Point(0, 2), Point(4, 2), Point(2, 0)]]
	# points[0].sort(key=get_point_order_key)
	# point_segments = split_points(points[0])
	# result = merge_segments(point_segments)

	segment_one_points = [Point(x=0, y=2), Point(x=2, y=0), Point(x=2, y=4), Point(x=2, y=6), Point(x=4, y=2)]
	segment_one_lines = [Line(Point(x=0, y=2),Point(x=2, y=0)), Line(Point(x=0, y=2),Point(x=2, y=4)), Line(Point(x=2, y=0),Point(x=2, y=4)), Line(Point(x=2, y=6),Point(x=4, y=2)), Line(Point(x=2, y=0),Point(x=4, y=2)), Line(Point(x=2, y=4),Point(x=4, y=2)), Line(Point(x=2, y=4),Point(x=2, y=6)), Line(Point(x=0, y=2),Point(x=2, y=6))]

	segment_two_points = [Point(x=6, y=6), Point(x=8, y=4), Point(x=10, y=0), Point(x=10, y=2), Point(x=10, y=6)]
	segment_two_lines = [Line(Point(x=6, y=6),Point(x=8, y=4)), Line(Point(x=6, y=6),Point(x=10, y=0)), Line(Point(x=8, y=4),Point(x=10, y=0)), Line(Point(x=10, y=2),Point(x=10, y=6)), Line(Point(x=10, y=0),Point(x=10, y=2)), Line(Point(x=8, y=4),Point(x=10, y=2)), Line(Point(x=8, y=4),Point(x=10, y=6)), Line(Point(x=6, y=6),Point(x=10, y=6))]

	segment_one = Segment(segment_one_points, segment_one_lines)
	segment_two = Segment(segment_two_points, segment_two_lines)

	result = merge_segments([segment_one, segment_two])

	print result

	# result_2 = merge_segments(result)
	# print result_2

# test_in_circumcirle()
test_case()

