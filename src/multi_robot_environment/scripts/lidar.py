#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy as np

lidar_data = None

def callback(data):
    global lidar_data
    lidar_data = data
    print(lidar_data.ranges)
    exit()

def plot_lidar():
    plt.ion()
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_ylim(0, 10)  # Lidarın maksimum menzilini ayarlayın
    line, = ax.plot([], [], 'bo')

    while not rospy.is_shutdown():
        if lidar_data:
            exit()
            angles = np.linspace(lidar_data.angle_min, lidar_data.angle_max, len(lidar_data.ranges))
            distances = np.array(lidar_data.ranges)

            # Veri aralıklarını güncelle
            line.set_xdata(angles)
            line.set_ydata(distances)

            # Grafiği güncelle
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.1)

def listener():
    rospy.init_node('lidar_listener', anonymous=True)
    rospy.Subscriber("/spur1/laser/scan", LaserScan, callback)
    plot_lidar()
    rospy.spin()

if __name__ == '__main__':
    listener()
