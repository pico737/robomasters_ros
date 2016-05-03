#!/usr/bin/env python

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from trapezoid.srv import *
from aimbot.msg import *

class AimBot:
	def __init__(self):

        # ---------------- setup ros ----------------
        # publishers
        self.pub_output_pose = rospy.Publisher('/aimbot/output_pose', PoseStamed, queue_size=10)

        # subscribers
        rospy.Subscriber('/aimbot/detected_enemy', DetectedRobot, self.handle_detected_enemy)

        # init the node
        rospy.init_node('aimbot', anonymous=True)

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()

    def handle_detected_enemy(self, data):
        print data.distance
        print data.y_rotation
        print data.z_rotation

if __name__ == '__main__':
	try:
        AimBot()
    except rospy.ROSInterruptException:
        pass