#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
import math

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha1 = connect("127.0.0.1:14550", wait_ready=True)

def takeoff(irtifa, iha):
    while iha.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)

    print("İHA arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")

    iha.armed = True

    while iha.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(0.5)

    print("İHA arm edildi.")

    iha.simple_takeoff(irtifa)
    
    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)

takeoff(40,iha1)

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
            (50, -150, 30),
            (50, -50, 30),
            (60, -50, 30),
            (60, -150, 30),
            (70, -150, 30),
            (70, -50, 30),
            (80, -50, 30),
            (80, -150, 30),
            (90, -150, 30),
            (90, -50, 30),
            (100, -50, 30),
            (100, -150, 30),
            (110, -150, 30),
            (110, -50, 30),
            (120, -50, 30),
            (120, -150, 30),
            (130, -150, 30),
            (130, -50, 30),
            (140, -50, 30),
            (140, -150, 30),
            (150, -150, 30),
            (150, -50, 30)
        ]
        self.waypoint_index = 0

        self.rate = rospy.Rate(3)  # 20 Hz

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
                break

            self.rate.sleep()

if __name__ == '__main__':
    navigator = DroneNavigator()
    navigator.navigate()
