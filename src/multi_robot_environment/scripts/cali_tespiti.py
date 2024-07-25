#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PoseStamped
import cv2
import threading
import numpy as np
import csv
from datetime import datetime
from std_msgs.msg import String

class ImageConverter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/webcam1/image_raw", Image, self.callback)
        self.pose_sub = rospy.Subscriber('/drone1/mavros/local_position/pose', PoseStamped, self.pose_callback)
        self.finish_sub = rospy.Subscriber('/drone_scan/finish', String, self.finish_callback)
        self.window_name = "Drone Camera View"
        self.lock = threading.Lock()
        self.cv_image = None
        self.cropped_image = None

        self.algilandi = False

        self.csv_file = open('drone_positions.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['timestamp', 'x', 'y', 'z'])


        # Create a window to display the image
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        self.display_thread = threading.Thread(target=self.display_image)
        self.display_thread.start()

    def finish_callback(self, data):
        if data.data == "finish":
            rospy.loginfo("Finish message received, shutting down.")
            rospy.signal_shutdown("Finish message received")


    def pose_callback(self, data):
        
        if self.algilandi:

            self.current_pose = data
            
            rospy.loginfo("Current position: x: %f, y: %f, z: %f",
                        self.current_pose.pose.position.x,
                        self.current_pose.pose.position.y,
                        self.current_pose.pose.position.z)
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.csv_writer.writerow([current_time,
                                      self.current_pose.pose.position.x,
                                      self.current_pose.pose.position.y,
                                      self.current_pose.pose.position.z])

            
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

                    height, width = self.cv_image.shape[:2]
    
                    # Kesilecek kısmın başlangıç noktalarını hesapla
                    start_x = width // 2 - 600 // 2
                    start_y = height // 2 - 500 // 2
                    
                    # Orta kısımdan 500x500'ü kes
                    self.cropped_image = self.cv_image[:, start_x:start_x+400]
                    

                    cv2.imshow("deneme", self.process(self.cropped_image))

                    
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
        upper_black = np.array([180, 255, 30])

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
            if area > 5000:
                x, y, w, h = cv2.boundingRect(contour)

                imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                self.algilandi = True
                return imageFrame
            
        self.algilandi = False
            
        return frame

def main():
    rospy.init_node('image_converter', anonymous=True)
    ic = ImageConverter()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    finally:
        ic.cleanup()

if __name__ == '__main__':
    main()
