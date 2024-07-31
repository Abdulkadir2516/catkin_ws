import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State

class Drone:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.state_sub = rospy.Subscriber(f"/{self.drone_id}/mavros/state", State, self.state_cb)
        self.pose_pub = rospy.Publisher(f"/{self.drone_id}/mavros/setpoint_position/local", PoseStamped, queue_size=10)
        self.pose = PoseStamped()
        self.state = State()
        
    def state_cb(self, msg):
        self.state = msg
        
    def set_pose(self, x, y, z):
        self.pose.pose.position.x = x
        self.pose.pose.position.y = y
        self.pose.pose.position.z = z
        self.pose_pub.publish(self.pose)



class FieldScanner:
    def __init__(self):
        rospy.init_node('field_scanner', anonymous=True)
        self.drone1 = Drone('drone1')
        self.drone2 = Drone('drone2')
        self.drone3 = Drone('drone3')
        
    def scan_field(self, drone1_waypoints, drone2_waypoints, drone3_waypoints):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            # Dronelar için waypointleri sırayla ziyaret et
            for wp1, wp2, wp3 in zip(drone1_waypoints, drone2_waypoints, drone3_waypoints):
                self.drone1.set_pose(*wp1)
                self.drone2.set_pose(*wp2)
                self.drone3.set_pose(*wp3)
                rospy.sleep(10)  # Droneların pozisyonuna ulaşması için bekleme süresi

            rate.sleep()

if __name__ == '__main__':
    try:
        scanner = FieldScanner()
        drone1_waypoints = [(0, 0, 10),(-30, 0, 10),(-30, 30, 10), (0, 30, 10)]
        drone2_waypoints = [(0, 0, 10),(-30, 0, 10),(-30, 30, 10), (0, 30, 10)]
        drone3_waypoints = [(0, 0, 10),(-30, 0, 10),(-30, 30, 10), (0, 30, 10)]
        scanner.scan_field(drone1_waypoints, drone2_waypoints, drone3_waypoints)
    except rospy.ROSInterruptException:
        pass
