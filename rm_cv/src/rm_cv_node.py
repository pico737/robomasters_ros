#!/usr/bin/env python

import math

# ros imports
import rospy
import tf
from aimbot.msg import *

# For this code to work, supply focal length and distance
# 
# Output angle in radian
# horangle outputs negative radians to rotate left
#          outputs positive radians to rotate right

# verangle outputs negative radians to move up
#          outputs positive radians to move down

# FOCAL_LENGTH_IPHONE = 28.0

class RmCv:
    def __init__(self, focal_length):
        self.focal_length = focal_length

        # ---------------- setup ros ----------------
        # publishers
        self.pub_detected_enemy = rospy.Publisher('/rm_cv/pub_detected_enemy', DetectedRobot, queue_size=10)

        # init the node
        rospy.init_node('rm_cv', anonymous=True)

        rospy.spin()

    def verangle(origin, actual, distance):
        yd = actual - origin
        yd = yd / self.focal_length
        return math.atan(yd/distance)

    def horangle(origin, actual, distance):
        xd = actual - origin #horizontal distance
        xd = xd / self.focal_length
        return math.asin(xd/distance)

if __name__ == '__main__':
    try:
        #Trapezoid('/dev/ttyACM0', 115200)
        RmCv(28.0)
    except rospy.ROSInterruptException:
        pass

# if __name__=='__main__':
#     rad = verangle(1160, 1771, 100.0)
#     print math.degrees(rad)
