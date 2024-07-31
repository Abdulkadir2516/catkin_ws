#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

class RobotPosition:
    def __init__(self):
        rospy.init_node('robot_position', anonymous=False)

        # Subscriber to get the robot's odometry
        rospy.Subscriber('/robot/robotnik_base_control/odom', Odometry, self.odom_callback)

        self.rate = rospy.Rate(1)  # 1 Hz

    def odom_callback(self, data):
        position = data.pose.pose.position
        print("Position: x = {:.2f}, y = {:.2f}".format(position.x, position.y))

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        robot_position = RobotPosition()
        robot_position.run()
    except rospy.ROSInterruptException:
        pass
