# !/usr/bin/env python2

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix, Imu
from mavros_msgs.msg import State, WaypointList
from geometry_msgs.msg import PoseStamped, TwistStamped

def gps_callback(data):
    rospy.loginfo("GPS Data: %s", data)

def imu_callback(data):
    rospy.loginfo("IMU Data: %s", data)

def state_callback(data):
    rospy.loginfo("State: %s", data)

def waypoint_callback(data):
    rospy.loginfo("Waypoints: %s", data)

def pose_callback(data):
    rospy.loginfo("Pose: %s", data)

def velocity_callback(data):
    rospy.loginfo("Velocity: %s", data)

def listener():
    rospy.init_node('data_listener', anonymous=True)

    rospy.Subscriber("/mavros/global_position/global", NavSatFix, gps_callback)
    rospy.Subscriber("/mavros/imu/data", Imu, imu_callback)
    rospy.Subscriber("/mavros/state", State, state_callback)
    rospy.Subscriber("/mavros/mission/waypoints", WaypointList, waypoint_callback)
    rospy.Subscriber("/mavros/local_position/pose", PoseStamped, pose_callback)
    rospy.Subscriber("/mavros/local_position/velocity_local", TwistStamped, velocity_callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
