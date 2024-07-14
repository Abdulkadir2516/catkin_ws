#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from message_filters import Subscriber, ApproximateTimeSynchronizer
import time
def callback(gps1_data):
    rospy.loginfo("Drone 1 GPS: Latitude: %f, Longitude: %f, Altitude: %f",
                  gps1_data.latitude, gps1_data.longitude, gps1_data.altitude)
    

def listener():
    rospy.init_node('gps_listener', anonymous=True)

    gps1_sub = Subscriber('/drone1/mavros/global_position/global', NavSatFix)

    ts = ApproximateTimeSynchronizer([gps1_sub], queue_size=10, slop=0.5)
    ts.registerCallback(callback)

    rospy.spin()
    
if __name__ == '__main__':
    listener()

