#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def publisher():
    # ROS düğümünü başlat
    rospy.init_node('publisher_node', anonymous=True)
    # String mesajları yayımlayacak bir yayıncı oluştur
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(1) # 1 Hz

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
