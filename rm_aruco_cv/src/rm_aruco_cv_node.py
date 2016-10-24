#!/usr/bin/env python

import time
import math

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from aimbot.msg import DetectedRobot

class RMAruco:
    def __init__(self):
        # class fields

        # publishers
        self.dr_pub = rospy.Publisher('/aimbot/detected_enemy', DetectedRobot, queue_size=10)

        # subscribers
        rospy.Subscriber('/ar_single_board/pose', PoseStamped, self.handle_pose)

        # init the node
        rospy.init_node('rm_aruco_cv', anonymous=True)

        rospy.spin()

    def handle_pose(self, data):
        # we're only interested in the position
        x_pos = data.pose.position.x
        y_pos = data.pose.position.y
        z_pos = data.pose.position.z

        dr_req = DetectedRobot()

        # distance
        dr_req.distance = z_pos

        # calculate y rotation
        # tan(theta) = y_pos / z_pos
        dr_req.y_rotation = -math.atan(y_pos / z_pos)

        # calculate z rotation
        # tan(theta) = x_pos / z_pos
        dr_req.z_rotation = math.atan(x_pos / z_pos)

        self.dr_pub.publish(dr_req)

if __name__ == '__main__':
    try:
        RMAruco()
    except rospy.ROSInterruptException:
        pass
