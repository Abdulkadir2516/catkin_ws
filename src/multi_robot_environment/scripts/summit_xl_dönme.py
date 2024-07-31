#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import atan2, pi

class RobotRotate:
    def __init__(self):
        rospy.init_node('robot_rotate', anonymous=False)

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

        # Convert quaternion to Euler angles
        self.yaw = self.quaternion_to_euler_yaw(self.orientation)

        # Print the yaw angle
        print("Yaw: {:.2f}".format(self.yaw))

    def quaternion_to_euler_yaw(self, orientation):
        # Extract the values from the quaternion
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        # Yaw calculation
        sin_yaw = 2.0 * (w * z + x * y)
        cos_yaw = 1.0 - 2.0 * (y * y + z * z)
        yaw = atan2(sin_yaw, cos_yaw)

        return yaw

    def rotate_continuously(self, angular_speed):
        vel_msg = Twist()
        vel_msg.angular.z = angular_speed

        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(vel_msg)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        robot_rotate = RobotRotate()
        rospy.loginfo("Waiting for odometry data...")
        while robot_rotate.position is None or robot_rotate.orientation is None:
            rospy.sleep(1)
        robot_rotate.rotate_continuously(0)  # Rotate at 0.5 rad/s
    except rospy.ROSInterruptException:
        pass
