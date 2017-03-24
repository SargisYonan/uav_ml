# main	
import map_driver
import knn

from pylab import *
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import time


#DRONES GET STUCK AT HOTSPOTS FIX THAT

def main():
	map_driver.place_interest_point(12, 12, 20)
	map_driver.place_interest_point(12, 16, 20)

	map_driver.plot_map(map_driver.master_map)

	map_driver.uav_flight(knn.predicted_map, 'collective_map.mp4')
	map_driver.plot_map(knn.predicted_map)


if __name__ == "__main__":
    main()