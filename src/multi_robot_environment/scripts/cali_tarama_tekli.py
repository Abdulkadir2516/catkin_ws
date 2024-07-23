#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
import math
from std_msgs.msg import String
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha1 = connect("127.0.0.1:14550", wait_ready=True)

class DroneNavigator:

    def __init__(self):
        rospy.init_node('drone_navigator')

        # Drone'un durumu ve pozisyonu için abonelikler
        self.state_sub = rospy.Subscriber('/drone1/mavros/state', State, self.state_callback)
        self.pose_sub = rospy.Subscriber('/drone1/mavros/local_position/pose', PoseStamped, self.pose_callback)
        self.local_pos_pub = rospy.Publisher('/drone1/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        self.current_state = State()
        self.current_pose = PoseStamped()
        self.target_pose = PoseStamped()
        # Hedef noktalar (x, y, z) formatında
        self.waypoints = [
            (-140, 50, 7),
            (-60, 50, 7)
        ]
        
        self.waypoint_index = 0
        self.rate = rospy.Rate(1)  # 1 Hz

    def state_callback(self, state):
        self.current_state = state

    def pose_callback(self, pose):
        self.current_pose = pose

    def distance_to_target(self):
        dx = self.target_pose.pose.position.x - self.current_pose.pose.position.x
        dy = self.target_pose.pose.position.y - self.current_pose.pose.position.y
        dz = self.target_pose.pose.position.z - self.current_pose.pose.position.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def set_target_pose(self, x, y, z):
        self.target_pose.pose.position.x = x
        self.target_pose.pose.position.y = y
        self.target_pose.pose.position.z = z
        self.target_pose.pose.orientation.w = 1.0  # Sabit bir yönelim için

    def navigate(self):
        while not rospy.is_shutdown():
            if self.waypoint_index < len(self.waypoints):
                current_waypoint = self.waypoints[self.waypoint_index]
                self.set_target_pose(*current_waypoint)
                self.local_pos_pub.publish(self.target_pose)
                if self.distance_to_target() < 0.5:  # Hedefe yakınlık kontrolü
                    rospy.loginfo("Reached waypoint %d", self.waypoint_index + 1)
                    self.waypoint_index += 1
            else:
                rospy.loginfo("All waypoints reached")
                pub = rospy.Publisher('/drone1/bitti', String, queue_size=10)
                rospy.loginfo("bitti")
                pub.publish("bitti")

                
                
                

            self.rate.sleep()
                
    
if __name__ == '__main__':
    navigator = DroneNavigator()
    navigator.navigate()
