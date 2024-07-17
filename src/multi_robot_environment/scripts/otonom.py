#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
import numpy as np

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance', anonymous=True)

        # Subscriber for Lidar data
        self.lidar_sub = rospy.Subscriber('/spur2/laser/scan', LaserScan, self.lidar_callback)
        # Publisher for drone velocity commands
        self.vel_pub = rospy.Publisher('/drone2/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        self.lidar_data = None
        self.rate = rospy.Rate(10)  # 10 Hz

    def lidar_callback(self, data):
        self.lidar_data = data

    def avoid_obstacles(self):
        while not rospy.is_shutdown():
            if self.lidar_data:
                distances = np.array(self.lidar_data.ranges)
                min_distance = np.min(distances)
                threshold_distance = 1.0  # Threshold distance to detect obstacles

                pose = PoseStamped()
                pose.header.frame_id = "map" # Frame ID'yi uygun şekilde ayarlayın
                pose.header.stamp = rospy.Time.now()

                if min_distance < threshold_distance:
                    # Obstacle detected, move backward and rotate
                    pose.pose.position.x = -0.2
                    pose.pose.orientation.z = 0.5
                else:
                    # No obstacle, move forward
                    pose.pose.position.x = 0.5
                    pose.pose.orientation.z = 0.0

                self.vel_pub.publish(pose)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        node = ObstacleAvoidance()
        node.avoid_obstacles()
    except rospy.ROSInterruptException:
        pass
