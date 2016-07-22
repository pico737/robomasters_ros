#!/usr/bin/env python

import time
import math
import subprocess

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from trapezoid.srv import *

class TrapezoidClient:
    def __init__(self):
        pub = rospy.Publisher('/trapezoid/setpoint_pose', PoseStamped, queue_size=10)
	#publ = rospy.Publisher('qtest', Point, queue_size = 10)
        rospy.init_node('trapezoid_client', anonymous=True)

        # wait for service
        print "waiting for /trapezoid/shoot service..."
        rospy.wait_for_service('/trapezoid/shoot')
        print "ok"

        # ex. call shoot service
        time.sleep(3)
        self.call_shoot_service()

        rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
	    #publ.publish(float(raw_input("drive")) , float(raw_input("strafe") , float(raw_input("rot")) )
	    #drive_req = float(raw_input("DRIVE"))
            #strafe_req = float(raw_input("strafe"))
            #rotate_req = float(raw_input("rotate"))
	    #publ.publish(drive_req,strafe_req,rotate_req)
            
            #convert roll, pitch, yaw to quaternion
            roll_req = 0
            pitch_req = float(raw_input("pitch"))
            yaw_req = float(raw_input("yaw"))
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
