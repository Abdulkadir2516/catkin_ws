#!/usr/bin/env python

import rospy
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import State
from geometry_msgs.msg import PoseStamped

current_state = State()

def state_cb(state):
    global current_state
    current_state = state

def set_mode(mode):
    rospy.wait_for_service('mavros/set_mode')
    try:
        set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)
        response = set_mode_client(custom_mode=mode)
        return response.mode_sent
    except rospy.ServiceException as e:
        rospy.logerr("Set mode failed: %s" % e)
        return False

def arm_drone():
    rospy.wait_for_service('mavros/cmd/arming')
    try:
        arm_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
        response = arm_client(True)
        return response.success
    except rospy.ServiceException as e:
        rospy.logerr("Arming failed: %s" % e)
        return False

def takeoff_drone():
    pose = PoseStamped()
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 2  # Desired takeoff altitude
    local_pos_pub.publish(pose)

if __name__ == '__main__':
    rospy.init_node('drone_control_node', anonymous=True)
    rospy.Subscriber('mavros/state', State, state_cb)
    local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)

    rate = rospy.Rate(20.0)
    while not current_state.connected:
        rate.sleep()

    rospy.loginfo("Drone connected")

    if set_mode("OFFBOARD") and arm_drone():
        rospy.loginfo("Drone armed and set to OFFBOARD mode")
        takeoff_drone()
        rospy.loginfo("Takeoff initiated")

    rospy.spin()
