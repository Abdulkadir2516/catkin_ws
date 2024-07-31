#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# Klavye girdisi için karakter eşlemeleri
MOVE_BINDINGS = {
    'w': (1, 0, 0, 0),  # İleri
    's': (-1, 0, 0, 0),  # Geri
    'a': (0, 0, 0, 1),  # Sol
    'd': (0, 0, 0, -1),  # Sağ
    'x': (0, 0, 0, 0),  # Durdur
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_twist_keyboard')
    pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=10)

    speed = 10
    turn = 3

    try:
        print("Control Your Robot!")
        print("Use WASD keys to move the robot")
        print("Press CTRL+C to quit")

        while True:
            key = getKey()
            if key in MOVE_BINDINGS.keys():
                x = MOVE_BINDINGS[key][0]
                y = MOVE_BINDINGS[key][1]
                z = MOVE_BINDINGS[key][2]
                th = MOVE_BINDINGS[key][3]
            else:
                x = 0
                y = 0
                z = 0
                th = 0
                if key == '\x03':  # CTRL+C
                    break

            twist = Twist()
            twist.linear.x = x * speed
            twist.linear.y = y * speed
            twist.linear.z = z * speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = th * turn
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
