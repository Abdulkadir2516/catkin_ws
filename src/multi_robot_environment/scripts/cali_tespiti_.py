#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image, NavSatFix
from cv_bridge import CvBridge, CvBridgeError
import cv2
import threading
from queue import Queue 
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from message_filters import Subscriber, ApproximateTimeSynchronizer

kontrol = False
koordinatlar = []
bridge = CvBridge()

# Her drone için görüntü kuyruğu
image_queue_1 = Queue()

def image_callback_1(msg):
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        image_queue_1.put(cv_image)
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))

def koordinatlari_gonder():
    global koordinatlar
    print(len(koordinatlar))

    for i in range(len(koordinatlar)-1):
        if(float(koordinatlar[i][0]) - float(koordinatlar[i+1][0]) > 5 or float(koordinatlar[i][1]) - float(koordinatlar[i+1][1]) > 5):
            print(koordinatlar[i])

def process_images():
    while not rospy.is_shutdown():
        if not image_queue_1.empty():
            cv_image = image_queue_1.get()
            cv2.imshow("Drone 1 Image Window", process(cv_image))
            if kontrol:    
                cv2.destroyAllWindows()
                koordinatlari_gonder()
                rospy.signal_shutdown("İşimiz bitti")
        cv2.waitKey(3)

def pose_callback(pose):
    global koordinatlar
    koordinatlar.append((pose.pose.position.x, pose.pose.position.y, pose.pose.position.z))
    print("x:{} \ny:{} \nz:{}".format(pose.pose.position.x, pose.pose.position.y, pose.pose.position.z))

def bitti(data):
    global kontrol
    kontrol = True

def process(src):
    global koordinatlar
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

    # Contur oluşturma ve renk takibi
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Drone'un koordinatlarını kaydet
            if len(koordinatlar) > 0:
                last_coordinates = koordinatlar[-1]
                rospy.loginfo("Detected at coordinates: x={}, y={}, z={}".format(last_coordinates[0], last_coordinates[1], last_coordinates[2]))
            
            return imageFrame

    return frame

def main():
    rospy.init_node('image_listener', anonymous=True)
    rospy.Subscriber("/webcam1/image_raw", Image, image_callback_1)
    pose_sub = rospy.Subscriber('/drone1/mavros/local_position/pose', PoseStamped, pose_callback)
    rospy.Subscriber('/drone1/bitti', String, bitti)

    # Create a separate thread to process OpenCV windows
    threading.Thread(target=process_images).start()

    rospy.spin()

if __name__ == '__main__':
    main()
