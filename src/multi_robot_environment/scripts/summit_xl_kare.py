#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import sqrt, pow, radians, atan2, pi

class RobotMove:
    def __init__(self):
        rospy.init_node('robot_move', anonymous=False)

        # Publisher to send velocity commands
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=10)

        # Subscriber to get the robot's odometry
        rospy.Subscriber('/robot/robotnik_base_control/odom', Odometry, self.odom_callback)

        self.rate = rospy.Rate(10)  # 10 Hz

        self.position = None
        self.orientation = None
        self.yaw = None

    def odom_callback(self, data):
        self.position = data.pose.pose.position
        self.orientation = data.pose.pose.orientation
        self.z = data.pose.pose.orientation.z
        self.w = data.pose.pose.orientation.w

        # Convert quaternion to Euler angles
        self.yaw = self.quaternion_to_euler_yaw(self.orientation)

    def quaternion_to_euler_yaw(self, orientation):
        # Extract the values from the quaternion
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        print("{:.2f},{:.2f},{:.2f},{:.2f},".format(x,y,z,w))

        # Yaw calculation
        sin_yaw = 2.0 * (w * z + x * y)
        cos_yaw = 1.0 - 2.0 * (y * y + z * z)
        yaw = atan2(sin_yaw, cos_yaw)

        return yaw

    def move_distance(self, distance, speed):
        vel_msg = Twist()
        vel_msg.linear.x = speed if distance > 0 else -speed
        initial_position = self.position.x if self.position else 0

        while self.position is None:
            rospy.sleep(1)

        while abs(self.position.x - initial_position) < abs(distance):
            self.cmd_vel_pub.publish(vel_msg)
            self.rate.sleep()

        # Stop the robot after reaching the distance
        vel_msg.linear.x = 0
        self.cmd_vel_pub.publish(vel_msg)

    def sol90(self, angular_speed):
        vel_msg = Twist()
        vel_msg.angular.z = angular_speed
        
        self.cmd_vel_pub.publish(vel_msg)

        while not(self.z > 0.9 and self.w < 0.1) :

            self.cmd_vel_pub.publish(vel_msg)
            self.rate.sleep()

        # Stop the robot after reaching the angle
        vel_msg.angular.z = 0
        self.cmd_vel_pub.publish(vel_msg)
    

        
    def run(self):
        rospy.loginfo("Waiting for odometry data...")
        while self.position is None:
            rospy.sleep(1)

        rospy.loginfo("Moving 40 meters forward")
        self.move_distance(40, 1)  # Move 40 meters forward at 0.5 m/s

        rospy.loginfo("Rotating 90 degrees left")
        self.sol90(3)  # Rotate 90 degrees left at 0.5 rad/s
        
        rospy.loginfo("Moving 40 meters forward")
        self.move_distance(40, 3)  # Move 40 meters forward at 0.5 m/s

        
if __name__ == '__main__':
    try:
        robot_move = RobotMove()
        robot_move.run()
    except rospy.ROSInterruptException:
        pass
