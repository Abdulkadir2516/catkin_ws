#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard %s", data.data)

def subscriber():
    # ROS düğümünü başlat
    rospy.init_node('subscriber_node', anonymous=True)
    # 'chatter' konusuna abone ol
    rospy.Subscriber('chatter', String, callback)
    # ROS'un çalışmaya devam etmesini sağla
    rospy.spin()

if __name__ == '__main__':
    subscriber()
