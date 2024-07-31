#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class MultiCameraViewer:
    def __init__(self):
        rospy.init_node('multi_camera_viewer', anonymous=True)

        self.bridge = CvBridge()

        # Subscribe to camera topics
        self.image_sub1 = rospy.Subscriber('/webcam1/image_raw', Image, self.callback1)
        self.image_sub2 = rospy.Subscriber('/webcam2/image_raw', Image, self.callback2)
        self.image_sub3 = rospy.Subscriber('/webcam3/image_raw', Image, self.callback3)
        self.image_sub4 = rospy.Subscriber('/robot/front_rgbd_camera/rgb/image_raw', Image, self.callback4)

        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None

    def callback1(self, data):
        self.image1 = self.bridge.imgmsg_to_cv2(data, 'bgr8')

    def callback2(self, data):
        self.image2 = self.bridge.imgmsg_to_cv2(data, 'bgr8')

    def callback3(self, data):
        self.image3 = self.bridge.imgmsg_to_cv2(data, 'bgr8')

    def callback4(self, data):
        self.image4 = self.bridge.imgmsg_to_cv2(data, 'bgr8')

    def show_images(self):
        while not rospy.is_shutdown():
            if self.image1 is not None:
                resized_frame1 = cv2.resize(self.image1, (400, 400))
                cv2.imshow('Camera 1', resized_frame1)
            if self.image2 is not None:
                resized_frame2 = cv2.resize(self.image2, (400, 400))
                cv2.imshow('Camera 2',resized_frame2 )
            if self.image3 is not None:
                resized_frame3 = cv2.resize(self.image3, (400, 400))

                cv2.imshow('Camera 3', resized_frame3)
            if self.image4 is not None:
                resized_frame4 = cv2.resize(self.image4, (400, 400))
                cv2.imshow('Camera 4', resized_frame4)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    viewer = MultiCameraViewer()
    viewer.show_images()
