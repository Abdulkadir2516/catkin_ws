#!/usr/bin/env python

import rospy
from mavros_msgs.msg import PositionTarget
from geometry_msgs.msg import PoseStamped
import time
from std_msgs.msg import String

class DroneScan:
    def __init__(self):
        rospy.init_node('drone_scan', anonymous=True)
        self.waypoint_pub = rospy.Publisher('/drone1/mavros/setpoint_raw/local', PositionTarget, queue_size=10)
        self.finish_pub = rospy.Publisher('/drone_scan/finish', String, queue_size=10)

        self.rate = rospy.Rate(10)  # 10 Hz
        self.waypoints = [
            (-10, -30, 10),
            (-10, -90, 10),
            (-20, -90, 10),
            (-20, -30, 10),
        ]

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
        drone_scan = DroneScan()
        rospy.sleep(2)  # Allow some time to receive the initial pose data
        drone_scan.run()
    except rospy.ROSInterruptException:
        pass
