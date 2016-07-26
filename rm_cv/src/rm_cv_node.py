#!/usr/bin/env python

import time
import pexpect
import sys

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from aimbot.msg import DetectedRobot

class RMCV:
    def __init__(self, enemy_color):
        # class fields

        # setup ros publishers and subscribers
        self.dr_pub = rospy.Publisher('/aimbot/detected_enemy', DetectedRobot, queue_size=10)
        rospy.init_node('rm_cv', anonymous=True)

        # call the cv program
        cv_process = pexpect.spawn("/home/pico/catkin_ws/src/robomasters_ros/rm_cv/src/client.py")

        while not rospy.is_shutdown():
            try:
                cv_process.expect('\n')
                line = cv_process.before.rstrip()
                if line == "---":
                    cv_process.expect('\n')
                    color = cv_process.before.rstrip()
                    cv_process.expect('\n')
                    distance = float(cv_process.before.rstrip())
                    cv_process.expect('\n')
                    y_rotation = float(cv_process.before.rstrip())
                    cv_process.expect('\n')
                    z_rotation = float(cv_process.before.rstrip())
                    if (color == enemy_color): # only shoot at enemy robots!
                        # publish the detected robot
                        dr_req = DetectedRobot()
                        dr_req.distance = distance
                        dr_req.y_rotation = y_rotation
                        dr_req.z_rotation = z_rotation
                        self.dr_pub.publish(dr_req)
            except pexpect.EOF:
                break
        print "ros shutdown"
        rospy.signal_shutdown("user shutdown command")

if __name__ == '__main__':
    try:
        if (len(sys.argv) == 2 and (sys.argv[1] == "red" or sys.argv[1] == "blue")):
            RMCV(sys.argv[1])
        else:
            print "usage: rm_cv_node.py <enemy_color>"
    except rospy.ROSInterruptException:
        pass
