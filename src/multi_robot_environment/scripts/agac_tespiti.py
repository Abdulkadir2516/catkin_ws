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
        # Ekranın bir resmini al ve BGR renk uzayına dönüştür
    frame = np.array(src)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    hsvFrame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2HSV)

    lower_line = np.array([4,162,134])
    upper_line = np.array([24,242,214])

    # Maskenizi tanımlayın
    mask = cv2.inRange(hsvFrame, lower_line, upper_line)

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

    cv2.imshow("ekran", result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        

def main():
    rospy.init_node('image_listener', anonymous=True)
    rospy.Subscriber("/webcam1/image_raw", Image, image_callback_1)
    
    # Create a separate thread to process OpenCV windows
    threading.Thread(target=process_images).start()

    rospy.spin()

if __name__ == '__main__':
    main()
