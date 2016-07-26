#!/usr/bin/env python

import time
import math
import threading
import subprocess

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
        cv_process = subprocess.Popen(["rm_darknet_yolo"], shell=True, stdout=subprocess.PIPE)

        #while not rospy.is_shutdown():
        while cv_process.poll() is None:
            line = cv_process.stdout.readline()
            if line == "---":
                color = cv_process.stdout.readline()
                distance = float(cv_process.stdout.readline())
                y_rotation = float(cv_process.stdout.readline())
                z_rotation = float(cv_process.stdout.readline())
                if (color == enemy_color): # only shoot at enemy robots!
                    # publish the detected robot
                    dr_req = DetectedRobot()
                    dr_req.distance = distance
                    dr_req.y_rotation = self.dr_y_rotation
                    dr_req.z_rotation = self.dr_z_rotation
                    self.dr_pub.publish(dr_req)

        print "ros shutdown"
        rospy.signal_shutdown("user shutdown command")

if __name__ == '__main__':
    try:
        RMCV('red')
    except rospy.ROSInterruptException:
        pass
