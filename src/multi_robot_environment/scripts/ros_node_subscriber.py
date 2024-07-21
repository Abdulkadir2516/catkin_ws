#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def callback(pose):
    rospy.loginfo("I heard %s", pose)

def subscriber():
    # ROS düğümünü başlat
    rospy.init_node('subscriber_node', anonymous=True)
    # 'chatter' konusuna abone ol
    rospy.Subscriber('cali_konumları', PoseStamped, callback)
    # ROS'un çalışmaya devam etmesini sağla
    rospy.spin()

if __name__ == '__main__':
    subscriber()
