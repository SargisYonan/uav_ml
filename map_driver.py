# You can save the animation using:
# ani.save('animation.mp4')
# Animated gif
# convert *.png animation.gif

import numpy as np
from pylab import *
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import time
import knn

grid_size = 50
hotspot_threshold = 0
master_map = np.zeros(shape=(grid_size, grid_size))
collective_map = -1 * np.ones(shape=(grid_size, grid_size))
hot_coordinates = []
cold_coordinates = []
max_poi_strength = 20
ignore_size = 3

class _uav:
	map = -1 * np.ones(shape=(grid_size, grid_size))
	def __init__(self, name, origin_lat, origin_long):
		self.name = name
		self.curr_lat = origin_lat
		self.curr_long = origin_long
		self.map[origin_lat, origin_long] = master_map[origin_lat, origin_long]
		self.long_inc = True
		self.last_pos = []
		collective_map[origin_lat, origin_long] = master_map[origin_lat, origin_long]

uav_one = _uav('Drone 1', 0, 0)
uav_two = _uav('Drone 2', 35, 0)
uav_three = _uav('Drone 3', 11, 12)

def uav_change_coordinates(uav, longitude, latitude):
	uav.last_pos.append([latitude, longitude])

	uav.curr_long = longitude
	uav.curr_lat = latitude

	uav.map[latitude, longitude] = master_map[latitude, longitude]
	collective_map[latitude, longitude] = master_map[latitude, longitude]
	if master_map[latitude, longitude] > hotspot_threshold and [latitude, longitude, master_map[latitude, longitude]] not in hot_coordinates:
		hot_coordinates.append([latitude, longitude, master_map[latitude, longitude]])
		print('Hotspot Found at: ' + str(latitude) + ', ' + str(longitude))
	else:
		if ([latitude, longitude] not in cold_coordinates):
			cold_coordinates.append([latitude, longitude])

def uav_linear_sweep(uav):
	last_long = uav.curr_long
	last_lat = uav.curr_lat

	if (uav.curr_lat < grid_size) or (uav.curr_long < grid_size):
		if uav.long_inc:
			if (uav.curr_long < grid_size - 1):
				uav_change_coordinates(uav, uav.curr_long + 1, uav.curr_lat)
				
				if (uav.curr_long == grid_size - 1):
					if uav.curr_lat < grid_size - 1:
						uav.curr_lat += 1
						if (uav.curr_long >= 0):
							uav_change_coordinates(uav, uav.curr_long, uav.curr_lat)
						uav.long_inc = False;
		else:
			if (uav.curr_long >= 0):
				uav_change_coordinates(uav, uav.curr_long - 1, uav.curr_lat)
				
				if (uav.curr_long == 0):
					if uav.curr_lat < grid_size - 1:
						uav.curr_lat += 1
						if (uav.curr_long < grid_size - 1):
							uav_change_coordinates(uav, uav.curr_long, uav.curr_lat)
						uav.long_inc = True;	

def classify_drone_directions(uav):
	curr_long = uav.curr_long
	curr_lat = uav.curr_lat

	hot = 0 # hot class
	cold = 0

	max_val = 0

	if (curr_lat < grid_size - 1 and curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat + 1, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long + 1
				move_to_lat = curr_lat + 1
				max_val = val

	if (curr_lat < grid_size - 1):
		val = knn.classify_point([curr_lat + 1, curr_long], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long
				move_to_lat = curr_lat + 1
				max_val = val
			
	if (curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long + 1
				move_to_lat = curr_lat
				max_val = val

	if (curr_lat > 0 and curr_long > 0):
		val = knn.classify_point([curr_lat - 1, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long - 1
				move_to_lat = curr_lat - 1
				max_val = val

	if (curr_lat > 0):
		val = knn.classify_point([curr_lat - 1, curr_long], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long
				move_to_lat = curr_lat - 1
				max_val = val

	if (curr_long > 0):
		val = knn.classify_point([curr_lat, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long - 1
				move_to_lat = curr_lat
				max_val = val

	if (curr_lat > 0 and curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat - 1, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long + 1
				move_to_lat = curr_lat - 1
				max_val = val

	if (curr_lat < grid_size - 1 and curr_long > 0):
		val = knn.classify_point([curr_lat + 1, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				move_to_long = curr_long - 1
				move_to_lat = curr_lat + 1
				max_val = val

	if max_val == cold:
		uav_linear_sweep(uav)
	else:
		uav_change_coordinates(uav, move_to_long, move_to_lat)

def classify_drone_directions_w_potentials(uav):
	curr_long = uav.curr_long
	curr_lat = uav.curr_lat

	move_to_long = 0
	move_to_lat = 0

	potential_max = 0
	potential_long = 0
	potential_lat = 0

	hot = 0 # hot class
	cold = 0

	max_val = 0


	if (curr_lat < grid_size - 1 and curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat + 1, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat + 1, curr_long + 1] in hot_coordinates or [curr_lat + 1, curr_long + 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat + 1
						potential_long = curr_long + 1
						potential_max = max_val
				else:
					move_to_long = curr_long + 1
					move_to_lat = curr_lat + 1
					max_val = val

	if (curr_lat < grid_size - 1):
		val = knn.classify_point([curr_lat + 1, curr_long], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat + 1, curr_long] in hot_coordinates or [curr_lat + 1, curr_long] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat + 1
						potential_long = curr_long
						potential_max = max_val
				else:
					move_to_long = curr_long
					move_to_lat = curr_lat + 1
					max_val = val
			
	if (curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat, curr_long + 1] in hot_coordinates or [curr_lat, curr_long + 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat
						potential_long = curr_long + 1
						potential_max = max_val
				else:
					move_to_long = curr_long + 1
					move_to_lat = curr_lat
					max_val = val

	if (curr_lat > 0 and curr_long > 0):
		val = knn.classify_point([curr_lat - 1, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat - 1, curr_long - 1] in hot_coordinates or [curr_lat - 1, curr_long - 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat - 1
						potential_long = curr_long - 1
						potential_max = max_val
				else:
					move_to_long = curr_long - 1
					move_to_lat = curr_lat - 1
					max_val = val

	if (curr_lat > 0):
		val = knn.classify_point([curr_lat - 1, curr_long], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat - 1, curr_long] in hot_coordinates or [curr_lat - 1, curr_long] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat - 1
						potential_long = curr_long
						potential_max = max_val
				else:
					move_to_long = curr_long
					move_to_lat = curr_lat - 1
					max_val = val

	if (curr_long > 0):
		val = knn.classify_point([curr_lat, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat, curr_long - 1] in hot_coordinates or [curr_lat, curr_long - 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat
						potential_long = curr_long - 1
						potential_max = max_val
				else:
					move_to_long = curr_long - 1
					move_to_lat = curr_lat
					max_val = val

	if (curr_lat > 0 and curr_long < grid_size - 1):
		val = knn.classify_point([curr_lat - 1, curr_long + 1], hot_coordinates, cold_coordinates)
		if [curr_lat - 1, curr_long + 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat - 1, curr_long + 1] in hot_coordinates or [curr_lat - 1, curr_long + 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat - 1
						potential_long = curr_long + 1
						potential_max = max_val
				else:
					move_to_long = curr_long + 1
					move_to_lat = curr_lat - 1
					max_val = val

	if (curr_lat < grid_size - 1 and curr_long > 0):
		val = knn.classify_point([curr_lat + 1, curr_long - 1], hot_coordinates, cold_coordinates)
		if [curr_lat + 1, curr_long - 1] in uav.last_pos[-ignore_size:]:
			val = 0
		elif val > hot:
			if (val > max_val):
				if ([curr_lat + 1, curr_long - 1] in hot_coordinates or [curr_lat + 1, curr_long - 1] in cold_coordinates):
					if (val > potential_max):
						potential_lat = curr_lat + 1
						potential_long = curr_long - 1
						potential_max = max_val
				else:
					move_to_long = curr_long - 1
					move_to_lat = curr_lat + 1
					max_val = val

	if max_val == cold:
		if potential_max == cold:
			uav_linear_sweep(uav)
		else:
			uav_change_coordinates(uav, potential_long, potential_lat)
	else:
		uav_change_coordinates(uav, move_to_long, move_to_lat)

def generate_data():
	classify_drone_directions_w_potentials(uav_one)
	classify_drone_directions_w_potentials(uav_two)
	classify_drone_directions_w_potentials(uav_three)
	knn.predict_map(hot_coordinates, cold_coordinates)

def data_gen():
    while True:
        yield generate_data()

# place_interest_point - radially places a fire or beacon
# at some point of interest
# INPUT: longitude - longitudinal axis of POI
# INPUT: latitude - latitudinal axis of POI
# INPUT: strength - strength of signal at the coordinates
#					must be less than or equal to max_poi_strength
def place_interest_point(longitude, latitude, strength):
	if (strength > max_poi_strength):
		print('error: strength parameter in place_interest_point() must be <= max_poi_strength')
		return

	if (latitude > grid_size - 1):
		print('error: latitude parameter in place_interest_point() must be < grid_size')
		return

	if (longitude > grid_size - 1):
		print('error: longitude parameter in place_interest_point() must be < grid_size')
		return

	radius_out = 0


	master_map[latitude, longitude] = strength
	if (latitude + radius_out < grid_size - 1) and (longitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude + radius_out] = strength
	
	if (longitude + radius_out < grid_size - 1):
		master_map[latitude, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude] = strength
	
	if (latitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude] = strength
	
	if (longitude - radius_out >= 0):
		master_map[latitude, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude + radius_out < grid_size - 1):
		master_map[latitude - radius_out, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1) and (longitude - radius_out >= 0):
		master_map[latitude + radius_out, longitude - radius_out] = strength

	radius_out += 1
	strength -= 1

	if (latitude + radius_out < grid_size - 1) and (longitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude + radius_out] = strength
	
	if (longitude + radius_out < grid_size - 1):
		master_map[latitude, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude] = strength
	
	if (latitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude] = strength
	
	if (longitude - radius_out >= 0):
		master_map[latitude, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude + radius_out < grid_size - 1):
		master_map[latitude - radius_out, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1) and (longitude - radius_out >= 0):
		master_map[latitude + radius_out, longitude - radius_out] = strength

	radius_out += 1
	strength -= 1

	if (latitude + radius_out < grid_size - 1) and (longitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude + radius_out] = strength
	
	if (longitude + radius_out < grid_size - 1):
		master_map[latitude, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude] = strength
	
	if (latitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude] = strength
	
	if (longitude - radius_out >= 0):
		master_map[latitude, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude - radius_out] = strength
	
	if (latitude - radius_out >= 0) and (longitude + radius_out < grid_size - 1):
		master_map[latitude - radius_out, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1) and (longitude - radius_out >= 0):
		master_map[latitude + radius_out, longitude - radius_out] = strength

	radius_out += 1
	strength -= 1

	if (longitude + radius_out < grid_size - 1):
		master_map[latitude, longitude + radius_out] = strength
	
	if (latitude + radius_out < grid_size - 1):
		master_map[latitude + radius_out, longitude] = strength
	
	if (latitude - radius_out >= 0):
		master_map[latitude - radius_out, longitude] = strength
	
	if (longitude - radius_out >= 0):
		master_map[latitude, longitude - radius_out] = strength

def uav_flight(map, filename):
	def update(data):
		mat = ax.matshow(map)
		return mat

	fig, ax = plt.subplots()
	mat = ax.matshow(map)
	#plt.colorbar(mat)
	speed = 1
	ani = animation.FuncAnimation(fig, update, data_gen, interval=speed,
                          save_count=50)
	#ani.save(filename, writer="ffmpeg", fps=3)	
	plt.show()

def plot_map(map):
	plt.imshow(map)
	plt.show()
