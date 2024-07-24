#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
import math
from dronekit import connect, VehicleMode
import time
import threading
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

def takeoff(irtifa, iha):
    while not iha.is_armable:
        print("{} arm edilebilir durumda değil.".format(iha))
        time.sleep(1)

    print("{} arm edilebilir.".format(iha))

    iha.mode = VehicleMode("GUIDED")
    iha.armed = True

    while not iha.armed:
        print("{} arm ediliyor...".format(iha))
        time.sleep(0.5)

    print("{} arm edildi.".format(iha))
    iha.simple_takeoff(irtifa)

    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print("{} hedefe yükseliyor.".format(iha))
        time.sleep(1)

class DroneNavigator:
    def __init__(self):
        self.bitis = False
        self.state_sub = rospy.Subscriber('/drone1/mavros/state', State, self.state_callback)
        self.pose_sub = rospy.Subscriber('/drone1/mavros/local_position/pose', PoseStamped, self.pose_callback)
        self.local_pos_pub = rospy.Publisher('/drone1/mavros/setpoint_position/local', PoseStamped, queue_size=10)

        self.current_state = State()
        self.current_pose = PoseStamped()
        self.target_pose = PoseStamped()
        self.waypoints = [
            (-140, 50, 7),
            (-60, 50, 7)
        ]

        self.waypoint_index = 0
        self.rate = rospy.Rate(0.1)  # 1 Hz

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
        self.target_pose.pose.orientation.w = 1.0

    def navigate(self):
        while not rospy.is_shutdown():
            if self.waypoint_index < len(self.waypoints):
                current_waypoint = self.waypoints[self.waypoint_index]
                self.set_target_pose(*current_waypoint)
                self.local_pos_pub.publish(self.target_pose)
                if self.distance_to_target() < 0.5:
                    rospy.loginfo("Reached waypoint %d", self.waypoint_index + 1)
                    self.waypoint_index += 1
            else:
                rospy.loginfo("All waypoints reached")
                break

            self.rate.sleep()

    def get_bitis(self):
        return self.bitis


class ImageConverter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/webcam1/image_raw", Image, self.callback)
        self.window_name = "Drone Camera View"
        self.lock = threading.Lock()
        self.cv_image = None

        # Create a window to display the image
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        self.display_thread = threading.Thread(target=self.display_image)
        self.display_thread.start()

    def callback(self, data):
        try:
            # Convert the ROS Image message to OpenCV format
            with self.lock:
                self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def display_image(self):
        while not rospy.is_shutdown():
            if self.cv_image is not None:
                with self.lock:
                    cv2.imshow(self.window_name, self.cv_image)
                    cv2.imshow("deneme", self.process(self.cv_image))
                cv2.waitKey(1)
                
        cv2.destroyAllWindows()

    def cleanup(self):
        with self.lock:
            self.cv_image = None
    
    def process(self,src):
            # Ekranın bir resmini al ve BGR renk uzayına dönüştür
        frame = np.array(src)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        hsvFrame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2HSV)

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Maskenizi tanımlayın
        mask = cv2.inRange(hsvFrame, lower_black, upper_black)

        # Maske üzerinden görüntüyü filtrele
        result = cv2.bitwise_and(frame, frame, mask=mask)


        kernel = np.ones((5, 5), "uint8")

        mask = cv2.dilate(mask, kernel)

        # contur oluşturma ve renk takibi
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 2000:
                x, y, w, h = cv2.boundingRect(contour)

                imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                return imageFrame
            
        return frame


def run_navigator():
    navigator = DroneNavigator()
    navigator.navigate()

def run_tespit():
    rospy.init_node('image_converter', anonymous=True)
    ic = ImageConverter()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    finally:
        ic.cleanup()

if __name__ == '__main__':
    rospy.init_node('multi_drone_node', anonymous=True)

    navigator_thread = threading.Thread(target=run_navigator)
    tespit_thread = threading.Thread(target=run_tespit)

    navigator_thread.start()
    tespit_thread.start()

    navigator_thread.join()
    tespit_thread.join()
