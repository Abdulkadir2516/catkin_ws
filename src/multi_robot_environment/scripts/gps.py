#!/usr/bin/env python

import rospy
from sensor_msgs.msg import NavSatFix
from message_filters import Subscriber, ApproximateTimeSynchronizer

def callback(gps1_data, gps2_data, gps3_data):
    rospy.loginfo("Drone 1 GPS: Latitude: %f, Longitude: %f, Altitude: %f",
                  gps1_data.latitude, gps1_data.longitude, gps1_data.altitude)
    rospy.loginfo("Drone 2 GPS: Latitude: %f, Longitude: %f, Altitude: %f",
                  gps2_data.latitude, gps2_data.longitude, gps2_data.altitude)
    rospy.loginfo("Drone 3 GPS: Latitude: %f, Longitude: %f, Altitude: %f",
                  gps3_data.latitude, gps3_data.longitude, gps3_data.altitude)

def listener():
    rospy.init_node('gps_listener', anonymous=True)

    gps1_sub = Subscriber('/drone1/mavros/global_position/global', NavSatFix)
    gps2_sub = Subscriber('/drone2/mavros/global_position/global', NavSatFix)
    gps3_sub = Subscriber('/drone3/mavros/global_position/global', NavSatFix)

    ts = ApproximateTimeSynchronizer([gps1_sub, gps2_sub, gps3_sub], queue_size=10, slop=0.1)
    ts.registerCallback(callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

