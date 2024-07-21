import rospy
from geometry_msgs.msg import Twist
import time

def move_straight(linear_speed, duration):
    velocity_msg = Twist()
    velocity_msg.linear.x = linear_speed
    velocity_msg.angular.z = 0
    velocity_publisher.publish(velocity_msg)
    time.sleep(duration)
    stop()

def turn(angle_speed, duration):
    velocity_msg = Twist()
    velocity_msg.linear.x = 0
    velocity_msg.angular.z = angle_speed
    velocity_publisher.publish(velocity_msg)
    time.sleep(duration)
    stop()

def stop():
    velocity_msg = Twist()
    velocity_msg.linear.x = 0
    velocity_msg.angular.z = 0
    velocity_publisher.publish(velocity_msg)
    time.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('square_motion', anonymous=True)
        velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Define parameters
        linear_speed = 0.5  # meters per second
        move_duration = 5   # seconds to move in a straight line
        angular_speed = 0.5  # radians per second
        turn_duration = 3.14 / 2 / angular_speed  # seconds to make a 90 degree turn

        for _ in range(4):
            move_straight(linear_speed, move_duration)
            turn(angular_speed, turn_duration)

       

    except rospy.ROSInterruptException:
        pass
