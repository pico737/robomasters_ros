#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def talker():
	pub = rospy.Publisher('/scan',LaserScan,queue_size = 100)
	rospy.init_node('talker',anonymous = True)
	rate = rospy.Rate(10)
	size = 20
	angle_inc = .3
	rang = []
	for i in range(1,21):
		if i< 5 or i > 15:
			rang.append(3)
		else:
			rang.append(10)
				
	while not rospy.is_shutdown():
		pub.publish(angle_increment = angle_inc , ranges = rang)
		


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
		
		
		
