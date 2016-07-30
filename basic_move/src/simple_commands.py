#!/usr/bin/env python
import rospy
import numpy as np
import math
import time
from sensor_msgs.msg import LaserScan
from follow_self import*
from basic_move.msg import Move


def listener():
    rospy.init_node('simple_commands', anonymous=True)
    rospy.Subscriber("/chassis_tomove", Move, easy)
    rospy.spin()

#dist and angle would be replaced by the properties of message
pub = rospy.Publisher('/trapezoid/setpoint_chassis', Point, queue_size=100)
def easy (data):
	if(data.angle is 0 and data.speed !=0 and data.dist!= 0):
		straight_line(data.dist,data.speed)
	elif(data.angle != 0 and data.speed != 0 and data.dist != 0):
		if(data.rot): #rotate 
			pub.publish(0,0,data.angle) #presumably it rotates in rad/sec
			time.sleep(1)
			straight_line(data.dist,data.speed)
		#this rot/strafe boolean won't be necessary when using lidar
		else:#strafe
			x = data.dist*math.cos(data.angle)
			pub.publish(0,data.speed,0)
			time.sleep(x/data.speed)
			straight_line(data.dist,data.speed)
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
