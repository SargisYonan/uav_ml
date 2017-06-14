# main	
import map_driver
import knn

from pylab import *
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import time

def main():

	map_driver.initialize_uavs(3)

	# place as many fires as you'd like
	#rand_lat = randint(0, map_driver.grid_size - 1)
	#rand_long = randint(0, map_driver.grid_size - 1)
	map_driver.place_interest_point(25, 25, 20)
	map_driver.place_interest_point(19, 25, 20)

	#rand_lat = randint(0, map_driver.grid_size - 1)
	#rand_long = randint(0, map_driver.grid_size - 1)
	#map_driver.place_interest_point(rand_lat, rand_long, 20)

	#rand_lat = randint(0, map_driver.grid_size - 1)
	#rand_long = randint(0, map_driver.grid_size - 1)
	#map_driver.place_interest_point(rand_lat, rand_long, 20)
	#map_driver.plot_map(map_driver.master_map)

	# UNCOMMENT ONE
	#### to see the map pov:
	#map_driver.uav_flight(map_driver.collective_map, 'collective_map.mp4')
	#### to see the KNN algorthm:
	map_driver.uav_flight(knn.predicted_map, 'predicted.mp4')
	
	# show the KNN map at the end
	map_driver.plot_map(knn.predicted_map)


if __name__ == "__main__":
    main()