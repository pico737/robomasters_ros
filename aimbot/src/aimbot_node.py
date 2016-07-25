#!/usr/bin/env python

import math
import time

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from trapezoid.srv import *
from aimbot.msg import *

class AimBot:
    def __init__(self):
        # constants
        self.max_yaw = math.pi / 2
        self.min_yaw = -math.pi / 2
        self.max_pitch = math.pi / 4
        self.min_pitch = -math.pi / 4

        # fields
        self.setpoint_yaw = 0    # the yaw setpoint in radians +right, -left
        self.setpoint_pitch = 0  # the pitch setpoint in radians +up, -down
        self.target_locked = False  # true when enemy lock is valid
        self.detected_enemy_timeout = 0  # timeout counter, timed out when 0

        # ---------------- setup ros ----------------
        # publishers
        self.pub_output_pose = rospy.Publisher('/trapezoid/setpoint_pose', PoseStamped, queue_size=10)

        # subscribers
        rospy.Subscriber('/aimbot/detected_enemy', DetectedRobot, self.handle_detected_enemy)

        # init the node
        rospy.init_node('aimbot', anonymous=True)

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.publish_output_pose()

            # timeout counter
            if (self.detected_enemy_timeout == 0):
                self.target_locked = False
                # TODO: return to center when timed out?
            else:
                self.detected_enemy_timeout -= 1

            rate.sleep()

    def handle_detected_enemy(self, data):
        self.detected_enemy_timeout = 10
        # print data.distance
        # print data.y_rotation
        # print data.z_rotation
        new_yaw = self.setpoint_yaw + data.z_rotation
        new_pitch = self.setpoint_pitch + data.y_rotation

        # check target locked
        new_yaw_valid = new_yaw < self.max_yaw and new_yaw > self.min_yaw
        new_pitch_valid = new_pitch < self.max_pitch and new_pitch > self.min_pitch
        self.target_locked = new_yaw_valid and new_pitch_valid

        # limit movement
        new_yaw = min(new_yaw, self.max_yaw)
        new_yaw = max(new_yaw, self.min_yaw)
        new_pitch = min(new_pitch, self.max_pitch)
        new_pitch = max(new_pitch, self.min_pitch)

        # TODO: distance correction kinematics

        self.setpoint_yaw = new_yaw
        self.setpoint_pitch = new_pitch

    def publish_output_pose(self):
        roll_send = 0
        pitch_send = self.setpoint_pitch
        yaw_send = self.setpoint_yaw

        # convert roll, pitch, yaw to quaternion
        quaternion_send = tf.transformations.quaternion_from_euler(roll_send, pitch_send, yaw_send)

        pose_send = PoseStamped()
        pose_send.header = Header()
        pose_send.pose.orientation.x = quaternion_send[0]
        pose_send.pose.orientation.y = quaternion_send[1]
        pose_send.pose.orientation.z = quaternion_send[2]
        pose_send.pose.orientation.w = quaternion_send[3]

        self.pub_output_pose.publish(pose_send)

if __name__ == '__main__':
    try:
        AimBot()
    except rospy.ROSInterruptException:
        pass