#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import time

def move_turtlebot():
    rospy.init_node('move_turtlebot3', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    move_cmd = Twist()
    
    for _ in range(4):
        # Move forward for 5 meters
        move_cmd.linear.x = 0.2  # Adjust speed as necessary
        move_cmd.angular.z = 0.0
        distance_moved = 0.0
        start_time = time.time()
        
        while distance_moved < 2.0:
            pub.publish(move_cmd)
            rate.sleep()
            current_time = time.time()
            distance_moved = 0.2 * (current_time - start_time)
        
        # Stop the robot before turning
        move_cmd.linear.x = 0.0
        pub.publish(move_cmd)
        rospy.sleep(1)

        # Rotate 90 degrees
        move_cmd.angular.z = 0.5  # Adjust angular speed as necessary
        angle_turned = 0.0
        start_time = time.time()
        
        while angle_turned < (3.14 / 2):
            pub.publish(move_cmd)
            rate.sleep()
            current_time = time.time()
            angle_turned = 0.5 * (current_time - start_time)
        
        # Stop the rotation
        move_cmd.angular.z = 0.0
        pub.publish(move_cmd)
        rospy.sleep(1)

    # Stop the robot finally
    move_cmd.linear.x = 0.0
    move_cmd.angular.z = 0.0
    pub.publish(move_cmd)

def odom_callback(data):
    rospy.loginfo("Pose: (%f, %f)", data.pose.pose.position.x, data.pose.pose.position.y)
    rospy.loginfo("Orientation: (%f, %f, %f, %f)", data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w)

def odom_listener():
    rospy.init_node('odom_listener', anonymous=True)
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.spin()

def scan_callback(data):
    rospy.loginfo("Laser Scan Data: %s", str(data.ranges))

def scan_listener():
    rospy.init_node('scan_listener', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        move_turtlebot()
    except rospy.ROSInterruptException:
        pass
