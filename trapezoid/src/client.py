#!/usr/bin/env python

import time
import math
import subprocess

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from trapezoid.srv import *

class TrapezoidClient:
    def __init__(self):
        pub = rospy.Publisher('/trapezoid/setpoint_pose', PoseStamped, queue_size=10)
        rospy.init_node('trapezoid_client', anonymous=True)

        # wait for service
        print "waiting for /trapezoid/shoot service..."
        rospy.wait_for_service('/trapezoid/shoot')
        print "ok"

        # ex. call shoot service
        time.sleep(3)
        self.call_shoot_service()

        rate = rospy.Rate(10) # 10hz

        # sets up reading coordinates on std out from cv code
        cmd = ["stdbuf", "-oL", "rosrun", "rm_cv","ZED_PROJECT"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        while not rospy.is_shutdown():
            # convert roll, pitch, yaw to quaternion
            roll_req = 0
            # pitch_req = 1.57
            # yaw_req = 1.0
            quaternion_req = tf.transformations.quaternion_from_euler(roll_req, pitch_req, yaw_req)

            pose_req = PoseStamped()
            pose_req.header = Header()
            pose_req.pose.orientation.x = quaternion_req[0]
            pose_req.pose.orientation.y = quaternion_req[1]
            pose_req.pose.orientation.z = quaternion_req[2]
            pose_req.pose.orientation.w = quaternion_req[3]
            #self.call_shoot_service()
            pub.publish(pose_req)
            rate.sleep()

            #process stdout to store cv info
            if p.poll() is None:
                line = p.stdout.readline()
                if line != "" and "ZED" not in line:
                    x_center,y_center,distance = line.split(", ")
                    pitch_req = -1 * y_center / distance
                    yaw_req = 1 * x_center / distance

                    #print ("Received: %d, %d, %d", x_center, y_center, distance)


    def call_shoot_service(self):
        try:
            shoot = rospy.ServiceProxy('/trapezoid/shoot', Shoot)
            pwm_speed = 99
            duration = 5
            shoot_response = shoot(pwm_speed, duration)
            return shoot_response.result
        except rospy.ServiceException, e:
            print "service call failed: %s"%e

if __name__ == '__main__':
    try:
        TrapezoidClient()
    except rospy.ROSInterruptException:
        pass
