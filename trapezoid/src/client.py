#!/usr/bin/env python

# ros imports
import rospy
import tf
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped

class TrapezoidClient:
    def __init__(self):
        pub = rospy.Publisher('/trapezoid/turret_pose', PoseStamped, queue_size=10)
        rospy.init_node('trapezoid_client', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            # convert roll, pitch, yaw to quaternion
            roll_req = 0
            pitch_req = 1
            yaw_req = 0
            quaternion_req = tf.transformations.quaternion_from_euler(roll_req, pitch_req, yaw_req)

            pose_req = PoseStamped()
            pose_req.header = Header()
            pose_req.pose.orientation.x = quaternion_req[0]
            pose_req.pose.orientation.y = quaternion_req[1]
            pose_req.pose.orientation.z = quaternion_req[2]
            pose_req.pose.orientation.w = quaternion_req[3]

            pub.publish(pose_req)
            rate.sleep()

if __name__ == '__main__':
    try:
        TrapezoidClient()
    except rospy.ROSInterruptException:
        pass
