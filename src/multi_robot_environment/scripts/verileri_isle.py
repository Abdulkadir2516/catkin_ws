#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
import csv
from geometry_msgs.msg import PoseStamped

# CSV dosyasını oluşturun ve başlıkları yazın
csv_file = open('pose_data.csv', mode='w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'position_x', 'position_y', 'position_z', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w'])

def callback(data):
    # Mesaj verilerini al
    timestamp = data.header.stamp.to_sec()
    position = data.pose.position
    orientation = data.pose.orientation
    
    print(data)
    # Verileri CSV dosyasına yaz
    csv_writer.writerow([timestamp, position.x, position.y, position.z, orientation.x, orientation.y, orientation.z, orientation.w])

def listener():
    # ROS düğümünü başlat
    rospy.init_node('pose_listener', anonymous=True)
    
    # PoseStamped mesajlarına abone ol
    rospy.Subscriber('/cali_konumlari', PoseStamped, callback)
    
    # Düğüm kapanırken CSV dosyasını kapat
    rospy.on_shutdown(lambda: csv_file.close())

    # Düğümün çalışmasını sağla
    rospy.spin()

if __name__ == '__main__':
    listener()
