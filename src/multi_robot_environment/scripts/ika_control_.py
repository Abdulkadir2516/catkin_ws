#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move():
    # ROS düğümünü başlat
    rospy.init_node('move_robot', anonymous=True)
    
    # /husky_velocity_controller/cmd_vel yayınını oluştur
    velocity_publisher = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
    
    # Bir Twist mesajı oluştur
    vel_msg = Twist()
    
    # Hız değerlerini ayarla (örneğin, ileri yönde 1 m/s ve sıfır dönüş)
    vel_msg.linear.x = -5.0
    vel_msg.linear.y = 0.0
    vel_msg.linear.z = 0.0
    vel_msg.angular.x = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.z = 0.0
    
    # Yayın hızını belirle
    rate = rospy.Rate(10) # 10 Hz

    while not rospy.is_shutdown():
        # Hız mesajını yayınla
        velocity_publisher.publish(vel_msg)
        
        # Belirtilen süre kadar bekle
        rate.sleep()

if __name__ == '__main__':
    try:
        # Robotu hareket ettir
        move()
    except rospy.ROSInterruptException:
        pass
