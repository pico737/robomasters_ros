#!/usr/bin/env python

import time
import math
import threading

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from aimbot.msg import DetectedRobot

class AimbotClient:
    def __init__(self):
        # class fields
        self.dr_distance = 0
        self.dr_y_rotation = 0
        self.dr_z_rotation = 0
        self.pause = 0

        # setup ros publishers and subscribers
        self.dr_pub = rospy.Publisher('/aimbot/detected_enemy', DetectedRobot, queue_size=10)
        rospy.init_node('aimbot_client', anonymous=True)

        # start a new thread for publishers
        pub_thread = threading.Thread(target=self.pub_process)
        pub_thread.start()

        print "type in command letter followed by value, or exit to quit"
        print "dr commands    rd: distance, ry: y_rotation, rz: z_rotation"
        print "test commands  tp: pause transmit for n seconds"
        print "ex: rd1.43"

        while not rospy.is_shutdown():
            cmd = raw_input("-->")
            if cmd == "exit":
                break
            else:
                value = float(cmd[2:])
                if cmd[0] == "r":
                    if cmd[1] == "d":
                        self.dr_distance = value
                    elif cmd[1] == "y":
                        self.dr_y_rotation = value
                    elif cmd[1] == "z":
                        self.dr_z_rotation = value
                    else:
                        print "command error"
                elif cmd[0] == "t":
                    if cmd[1] == "p":
                        self.pause = 1
                        time.sleep(value)
                        self.pause = 0
                    else:
                        print "command error"
                else:
                    print "command error"
        print "ros shutdown"
        rospy.signal_shutdown("user shutdown command")

    def pub_process(self):
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # (1) publish dr commands
            if self.pause == 0:
                dr_req = DetectedRobot()
                dr_req.distance = self.dr_distance
                dr_req.y_rotation = self.dr_y_rotation
                dr_req.z_rotation = self.dr_z_rotation
                self.dr_pub.publish(dr_req)
            rate.sleep()

if __name__ == '__main__':
    try:
        AimbotClient()
    except rospy.ROSInterruptException:
        pass
