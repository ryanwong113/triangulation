from triangulation import *

def test_case():
	points = [[Point(2, 6), Point(6, 6), Point(10, 6), Point(2, 4), Point(8, 4), Point(0, 2), Point(4, 2), Point(10, 2), Point(2, 0), Point(10, 0)]]
	# points = [[Point(6, 6), Point(10, 6), Point(8, 4), Point(10, 2), Point(10, 0)]]
	# points = [[Point(2, 6), Point(2, 4), Point(0, 2), Point(4, 2), Point(2, 0)]]
	points[0].sort(key=get_point_order_key)
	point_segments = split_points(points[0])
	result = merge_segments(point_segments)
	plot_matplotlib(result)

# Initialisation
def init():
	range_min = 1
	range_max = 50
	num_of_points = 10
	points = [[]]
	for i in range(0, num_of_points):
		while True:
			new_point = Point(random.randint(range_min, range_max), random.randint(range_min, range_max))
			if new_point not in points[0]:
				points[0].append(new_point)
				break
	points[0].sort(key=get_point_order_key)
	point_segments = split_points(points[0])
	result = merge_segments(point_segments)
	plot_matplotlib(result)

# test_case()
for i in [1, 2, 3]:
	init()
