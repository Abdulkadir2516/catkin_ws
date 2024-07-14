#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from sensor_msgs.msg import NavSatFix
from std_srvs.srv import Empty, EmptyResponse
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

iha2 = connect("127.0.0.1:14560", wait_ready=True)
iha1 = connect("127.0.0.1:14550", wait_ready=True)
iha3 = connect("127.0.0.1:14570", wait_ready=True)

def takeoff(irtifa, iha):
    while iha.is_armable is not True:
        print(f"{iha} arm edilebilir durumda değil.")
        time.sleep(1)

    print(f"{iha} arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")

    iha.armed = True

    while iha.armed is not True:
        print(f"{iha} arm ediliyor...")
        time.sleep(0.5)

    print(f"{iha} arm edildi.")

    iha.simple_takeoff(irtifa)
    
    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print(f"{iha} hedefe yükseliyor.")
        time.sleep(1)
"""
# Thread'leri oluştur
takeoff_threads = []

for iha in [iha1, iha2, iha3]:#
    takeoff_thread = threading.Thread(target=takeoff, args=(9, iha))
    takeoff_threads.append(takeoff_thread)
    

# Kalkış thread'lerini başlat
for thread in takeoff_threads:
    thread.start()

# Kalkış thread'lerinin bitmesini bekle
for thread in takeoff_threads:  
    thread.join()"""

class DroneController:
    def __init__(self):
        rospy.init_node('drone_controller')

        # Drone1 için abonelikler ve yayıncılar
        self.state_sub1 = rospy.Subscriber('/drone1/mavros/state', State, self.state_callback1)
        self.pose_sub1 = rospy.Subscriber('/drone1/mavros/local_position/pose', PoseStamped, self.pose_callback1)
        self.local_pos_pub1 = rospy.Publisher('/drone1/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        # Drone2 için abonelikler ve yayıncılar
        self.state_sub2 = rospy.Subscriber('/drone2/mavros/state', State, self.state_callback2)
        self.pose_sub2 = rospy.Subscriber('/drone2/mavros/local_position/pose', PoseStamped, self.pose_callback2)
        self.local_pos_pub2 = rospy.Publisher('/drone2/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        # Acil durum durdurma servisi
        self.emergency_stop_service = rospy.Service('emergency_stop', Empty, self.handle_emergency_stop)

        self.current_pose1 = PoseStamped()
        self.current_pose2 = PoseStamped()
        self.target_pose1 = PoseStamped()
        self.target_pose2 = PoseStamped()

        self.safe_distance = 2.0  # Çarpışmayı önlemek için minimum mesafe
        self.emergency_stop = False

        self.rate = rospy.Rate(20)

    def state_callback1(self, state):
        self.state1 = state

    def state_callback2(self, state):
        self.state2 = state

    def pose_callback1(self, pose):
        self.current_pose1 = pose

    def pose_callback2(self, pose):
        self.current_pose2 = pose

    def calculate_distance(self, pose1, pose2):
        return math.sqrt((pose1.pose.position.x - pose2.pose.position.x)**2 + 
                         (pose1.pose.position.y - pose2.pose.position.y)**2 + 
                         (pose1.pose.position.z - pose2.pose.position.z)**2)

    def handle_emergency_stop(self, req):
        rospy.loginfo("Emergency stop triggered!")
        self.emergency_stop = True
        return EmptyResponse()

    def send_target_position(self, drone_id, target_pose):
        if drone_id == 1:
            self.local_pos_pub1.publish(target_pose)
        elif drone_id == 2:
            self.local_pos_pub2.publish(target_pose)

    def move_drones(self):
        while not rospy.is_shutdown():
            distance = self.calculate_distance(self.current_pose1, self.current_pose2)
            rospy.loginfo("Distance between drones: %f", distance)

            if self.emergency_stop or distance < self.safe_distance:
                print("dronelar birbirine çok yakın", distance)
                self.target_pose1.pose.position.x = self.current_pose1.pose.position.x
                self.target_pose1.pose.position.y = self.current_pose1.pose.position.y
                self.target_pose1.pose.position.z = self.current_pose1.pose.position.z

                self.target_pose2.pose.position.x = self.current_pose2.pose.position.x
                self.target_pose2.pose.position.y = self.current_pose2.pose.position.y
                self.target_pose2.pose.position.z = self.current_pose2.pose.position.z
            else:
                self.target_pose1.pose.position.x = 10.0  # Belirli bir koordinat örneği
                self.target_pose1.pose.position.y = 10.0
                self.target_pose1.pose.position.z = 10.0

                self.target_pose2.pose.position.x = 10.0  # Belirli bir koordinat örneği
                self.target_pose2.pose.position.y = 10.0
                self.target_pose2.pose.position.z = 10.0

            self.send_target_position(1, self.target_pose1)
            self.send_target_position(2, self.target_pose2)







            self.rate.sleep()

if __name__ == '__main__':
    controller = DroneController()
    controller.move_drones()
