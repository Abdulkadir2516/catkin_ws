import pandas as pd



import rospy
from mavros_msgs.msg import PositionTarget
from geometry_msgs.msg import PoseStamped
import time
from std_msgs.msg import String

class DroneScan2:

    def __init__(self):
        rospy.init_node('drone_scan2', anonymous=True)
        self.waypoint_pub = rospy.Publisher('/drone2/mavros/setpoint_raw/local', PositionTarget, queue_size=10)
        self.finish_pub = rospy.Publisher('/drone_scan2/finish', String, queue_size=10)

        self.rate = rospy.Rate(10)  # 10 Hz
        self.waypoints = self.get_waypoints()  # Verilen waypoint'leri kullan
    
    def get_waypoints(self):
        # CSV dosyasından veriyi okuyalım
        df = pd.read_csv('~/drone_positions.csv')

        # Yeni sütunlar oluşturmak için listeler
        average_y = []
        x_values = []

        # Başlangıç değerleri
        previous_y = df['y'].iloc[0]
        previous_x = df['x'].iloc[0]
        temp_values_y = [previous_y]
        temp_values_x = [previous_x]

        # y değerlerinin arasındaki farkı kontrol ederek ortalama hesaplayalım ve x değerlerini ekleyelim
        for x, y in zip(df['x'].iloc[1:], df['y'].iloc[1:]):
            if abs(y - previous_y) < 1.2:
                temp_values_y.append(y)
                temp_values_x.append(x)
            else:
                if temp_values_y:
                    average_y.append(sum(temp_values_y) / len(temp_values_y))
                    x_values.append(temp_values_x[0])  # İlk x değerini ekle
                    temp_values_y = [y]
                    temp_values_x = [x]
                else:
                    average_y.append(y)
                    x_values.append(x)
            previous_y = y

        # Son grubu da ekleyelim
        if temp_values_y:
            average_y.append(sum(temp_values_y) / len(temp_values_y))
            x_values.append(temp_values_x[0])

        # Ortalamaları ve x değerlerini yeni sütunlar olarak ekleyelim
        df['x_values'] = pd.Series(x_values)
        df['average_y'] = pd.Series(average_y)

        # Sonucu yeni bir CSV dosyasına kaydedelim
        df.to_csv('./processed_data.csv', index=False)

        # Waypoint'ler oluşturmak için
        waypoints = [(x - 5, y, 5) for x, y in zip(x_values,average_y)]

        print("Waypoints:", waypoints)
        return waypoints

    def set_waypoint(self, x, y, z):
        waypoint = PositionTarget()
        waypoint.header.stamp = rospy.Time.now()
        waypoint.coordinate_frame = PositionTarget.FRAME_LOCAL_NED
        waypoint.type_mask = PositionTarget.IGNORE_VX + PositionTarget.IGNORE_VY + PositionTarget.IGNORE_VZ + \
                             PositionTarget.IGNORE_AFX + PositionTarget.IGNORE_AFY + PositionTarget.IGNORE_AFZ + \
                             PositionTarget.IGNORE_YAW_RATE
        waypoint.position.x = x
        waypoint.position.y = y
        waypoint.position.z = z
        waypoint.yaw = 0  # Yaw angle can be adjusted as needed
        return waypoint

    def run(self):
        for waypoint in self.waypoints:
            wp_msg = self.set_waypoint(waypoint[0], waypoint[1], waypoint[2])
            for _ in range(100):
                self.waypoint_pub.publish(wp_msg)
                self.rate.sleep()
            rospy.loginfo("Waypoint %s reached", waypoint)
            time.sleep(20)  # Give some time to reach the waypoint

        # Tarama işlemi bittiğinde "finish" mesajı yayınla
        self.finish_pub.publish("finish")
        rospy.loginfo("Scan finished, finish message published.")
        #rospy.signal_shutdown("Scan finished")

if __name__ == '__main__':
    try:
        drone_scan = DroneScan2()
        rospy.sleep(2)  # Allow some time to receive the initial pose data
        drone_scan.run()
    except rospy.ROSInterruptException:
        pass
