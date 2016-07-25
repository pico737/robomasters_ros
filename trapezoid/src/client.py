#!/usr/bin/env python

import time
import math
import threading

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from trapezoid.srv import *
from trapezoid.msg import *

class TrapezoidClient:
    def __init__(self):
        # class fields
        self.roll_req = 0
        self.pitch_req = 0
        self.yaw_req = 0
        self.drive_req = 0
        self.strafe_req = 0
        self.rotate_req = 0
        self.feeder_req = 0

        # setup ros publishers and subscribers
        self.setpoint_pose_pub = rospy.Publisher('/trapezoid/setpoint_pose', PoseStamped, queue_size=10)
        self.setpoint_chassis_pub = rospy.Publisher('/trapezoid/setpoint_chassis', Point, queue_size=10)
        self.setpoint_shoot_pub = rospy.Publisher('/trapezoid/setpoint_shoot', Shooting, queue_size=10)
        rospy.init_node('trapezoid_client', anonymous=True)

        # start a new thread for publishers
        pub_thread = threading.Thread(target=self.pub_process)
        pub_thread.start()

        print "type in command letter followed by value, or exit to quit"
        print "turret commands    tr: roll, tp: pitch, ty: yaw"
        print "chassis commands   cd: drive, cs: strafe, cr: rotate"
        print "shooting commands  sf: feeder motor (1 or 0)"
        print "ex: tr1.43"

        while not rospy.is_shutdown():
            cmd = raw_input("-->")
            if cmd == "exit":
                break
            else:
                value = float(cmd[2:])
                if cmd[0] == "t":
                    if cmd[1] == "r":
                        self.roll_req = value
                    elif cmd[1] == "p":
                        self.pitch_req = value
                    elif cmd[1] == "y":
                        self.yaw_req = value
                    else:
                        print "command error"
                elif cmd[0] == "c":
                    if cmd[1] == "d":
                        self.drive_req = value
                    elif cmd[1] == "s":
                        self.strafe_req = value
                    elif cmd[1] == "r":
                        self.rotate_req = value
                    else:
                        print "command error"
                elif cmd[0] == "s":
                    if cmd[1] == "f":
                        self.feeder_req = value
                else:
                    print "command error"
        print "ros shutdown"
        rospy.signal_shutdown("user shutdown command")

    def pub_process(self):
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # (1) publish turret commands
            #convert roll, pitch, yaw to quaternion
            quaternion_req = tf.transformations.quaternion_from_euler(self.roll_req, self.pitch_req, self.yaw_req)

            pose_req = PoseStamped()
            pose_req.header = Header()
            pose_req.pose.orientation.x = quaternion_req[0]
            pose_req.pose.orientation.y = quaternion_req[1]
            pose_req.pose.orientation.z = quaternion_req[2]
            pose_req.pose.orientation.w = quaternion_req[3]
            self.setpoint_pose_pub.publish(pose_req)

            # (2) publish chassis commands
            chassis_req = Point()
            chassis_req.x = self.drive_req
            chassis_req.y = self.strafe_req
            chassis_req.z = self.rotate_req
            self.setpoint_chassis_pub.publish(chassis_req)

            # (3) publish shooting commands
            shoot_req = Shooting()
            shoot_req.feeder_motor_state = self.feeder_req
            shoot_req.friction_motor_state = 0
            self.setpoint_shoot_pub.publish(shoot_req)

            rate.sleep()

    # shoot service is deprecated, don't call this function
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
