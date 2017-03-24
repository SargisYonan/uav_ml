max_dist = 50

grid_size = 50

import numpy as np

predicted_map = np.zeros(shape=(grid_size, grid_size))


def euclidean_distance(point_a, point_b):
	a = abs(point_a[0] - point_b[0])
	b = abs(point_a[1] - point_b[1])

	return (a**2 + b**2)**.5

def classify_point(point, list_poi_1, list_poi_2):
	p1_dist = 0

	class_two = 0
	class_one = 0

	for p1 in list_poi_1:
		dist = euclidean_distance([p1[1], p1[0]], [point[1], point[0]])
		if (dist < max_dist and dist > 0):
			class_one += p1[2]/dist

	for p2 in list_poi_2:
		dist = euclidean_distance([p2[1], p2[0]], [point[1], point[0]])
		if (dist < max_dist and dist > 0):
			class_two += 1/dist

	if (class_one > class_two):
		return class_one
	else:
		return 0

def predict_map(list_poi_1, list_poi_2):
	for i in range(grid_size):
		for j in range(grid_size):
			predicted_map[i, j] = classify_point([i, j], list_poi_1, list_poi_2)

