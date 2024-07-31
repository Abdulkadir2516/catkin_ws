#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time

def move_square():
    rospy.init_node('move_square', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Kare çizmek için ayarlar
    speed = 10  # m/s
    distance = 50  # metre
    angle = 90  # derece
    angular_speed = 1  # rad/s

    for _ in range(4):
        # İleri gitme
        vel_msg.linear.x = speed
        vel_msg.angular.z = 0
        distance_traveled = 0
        t0 = rospy.Time.now().to_sec()

        while distance_traveled < distance:
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            distance_traveled = speed * (t1 - t0)

        # Durdurma
        vel_msg.linear.x = 0
        velocity_publisher.publish(vel_msg)
        time.sleep(1)

        # 90 derece döndürme
        vel_msg.angular.z = angular_speed
        angular_distance = 0
        t0 = rospy.Time.now().to_sec()

        while angular_distance < (angle * 2 * 3.14 / 360):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            angular_distance = angular_speed * (t1 - t0)

        # Durdurma
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        time.sleep(1)


    # Hareketi durdurma
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        move_square()
    except rospy.ROSInterruptException:
        pass
