#!/usr/bin/env python

import time
import math
import threading
import random

# ros imports
import rospy
from geometry_msgs.msg import Point

class BaseMove:
    def __init__(self):
        # class constants
        self.drive_const = 100
        self.strafe_const = 100
        self.rotate_const = 100
        self.time_between_move_s = 1

        # class fields
        self.drive_req = 0
        self.strafe_req = 0
        self.rotate_req = 0

        # setup ros publishers and subscribers
        self.setpoint_chassis_pub = rospy.Publisher('/trapezoid/setpoint_chassis', Point, queue_size=10)
        rospy.init_node('base_move', anonymous=True)

        # start a new thread for publishers
        pub_thread = threading.Thread(target=self.pub_process)
        pub_thread.start()

        # main control loop
        while not rospy.is_shutdown():
            # generate choices
            drive_choice = random.randint(-1, 1)
            strafe_choice = random.randint(-1, 1)
            rotate_choice = random.randint(-1, 1)

            # apply choices
            self.drive_req = drive_choice * self.drive_const
            self.strafe_req = strafe_choice * self.strafe_const
            self.rotate_req = rotate_choice * self.rotate_const

            # wait time interval
            time.sleep(self.time_between_move_s)

    def pub_process(self):
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # publish chassis commands
            chassis_req = Point()
            chassis_req.x = self.drive_req
            chassis_req.y = self.strafe_req
            chassis_req.z = self.rotate_req
            self.setpoint_chassis_pub.publish(chassis_req)

if __name__ == '__main__':
    try:
        BaseMove()
    except rospy.ROSInterruptException:
        pass