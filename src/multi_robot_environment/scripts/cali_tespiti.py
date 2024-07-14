#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import threading
from queue import Queue  # Python 2'de 'queue' yerine 'Queue' kullanılır
import numpy as np

bridge = CvBridge()

# Her drone için görüntü kuyruğu
image_queue_1 = Queue()

def image_callback_1(msg):
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        image_queue_1.put(cv_image)
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))

def process_images():
    while not rospy.is_shutdown():
        if not image_queue_1.empty():
            cv_image = image_queue_1.get()
            cv2.imshow("Drone 1 Image Window", process(cv_image))
        
        cv2.waitKey(3)

def process(src):
    frame = np.array(src)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    _, thresh = cv2.threshold(gray, 0,100, cv2.THRESH_OTSU)

     # contur oluşturma ve renk takibi
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return imageFrame

    return frame

def main():
    rospy.init_node('image_listener', anonymous=True)
    rospy.Subscriber("/webcam1/image_raw", Image, image_callback_1)
    
    # Create a separate thread to process OpenCV windows
    threading.Thread(target=process_images).start()

    rospy.spin()

if __name__ == '__main__':
    main()
