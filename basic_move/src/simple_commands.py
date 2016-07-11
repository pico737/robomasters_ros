#!/usr/bin/env python
import rospy
import numpy as np
import math
import time
from sensor_msgs.msg import LaserScan
import Move
#from nav_msgs.msg import Odometry
dist = 3
angle = 0
speed = 3
rot = false

#dist and angle would be replaced by the properties of message
#I just use 'wheel_control()' here, but it'll likely be changed
pub = rospy.Publisher('/move_simple', Move, queue_size=100)
def easy (dist,angle,speed,rot):
	if(angle is 0 and speed not 0 and dist not 0):
		straight_line(dist,speed)
	elif(angle not 0 and speed not 0 and dist not 0):
		if(rot): #rotate 
			pub.publish(0,0,angle) #presumably it rotates in rad/sec
			time.sleep(1)
			straight_line(dist,speed)
		#this rot/strafe boolean won't be necessary when using lidar
		else:#strafe
			x = dist*math.cos(angle)
			pub.publish(0,speed,0)
			time.sleep(x/speed)
			straight_line(dist,speed)
	else:
		pub.publish(0,0,0)
			

def straight_line(dist,speed):
		pub.publish(speed,0,0) 
		time.sleep(dist/speed) #'sleeps' for the amount of time it takes to travel given distance, then sets all speeds to 0
		#This can be replaced/enhanced with odometry, since it's right now not very accurate.
		pub.publish(0,0,0)









#def listener():
    #rospy.init_node('listener', anonymous=True)
    #rospy.Subscriber("/aim", SomeThing, simple)
    #rospy.spin()