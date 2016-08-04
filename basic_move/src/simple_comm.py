#!/usr/bin/env python
import rospy
import numpy as np
import math
import time
from sensor_msgs.msg import LaserScan
from follow_self import*
from basic_move.msg import Move


bot = 2
def listener():
    rospy.init_node('simple_commands', anonymous=True)
    rospy.Subscriber("/chassis_tomove", Move, tomove_handle)
    rospy.Subscriber('/scan',LaserScan,handle_scan)
    rospy.spin()

#TODO: fix the time.sleeps
#dist and angle would be replaced by the properties of message
pub = rospy.Publisher('/trapezoid/setpoint_chassis', Point, queue_size=100)

def tomove_handle(data):
	easy(data,null)

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

			

def handle_scan(data):
	farthest = move_pos(data)
 	angle = data.angle_increment*(farthest[bot-1]+farthest[0])/2
 	pub.publish(50,0,angle)




def straight_line(dist,speed):
		pub.publish(speed,0,0) 
		time.sleep(dist/speed) #'sleeps' for the amount of time it takes to travel given distance, then sets all speeds to 0
		#This can be replaced/enhanced with odometry, since it's right now not very accurate.
		pub.publish(0,0,0), 

def move_pos(scan):

    time = 0
    max = 0
    pos = 0
    current_angle = 0
    currentLength = 0
    checkerold = []
    checkernew = [] #temp
    indiceold = []
    indicenew = []#temp
    for i, item in enumerate(scan.ranges):
    	average = scan.ranges[0]
    	time+=1
    	current_angle = (scan.angle_increment*time)
        if scan.ranges[i] > (average):
            if(currentLength==0):
                checkernew = []
                indicenew = []
            currentLength+=1
            if currentLength > max:
                max = currentLength
            checkernew.append(item)
            indicenew.append(i)
        else:
            if(max==currentLength and max > 0):
                checkerold = checkernew
                indiceold = indicenew
            	average = sum(checkerold)/len(checkerold)
            currentLength = 0
    pos = 0
    shape = len(indiceold)
    if(shape > 0):
	    if(shape %2 ==0):
	    	pos = ((checkerold[shape/2]) + (checkerold[shape/2 - 1]))/2
	    else:
	    	pos = (checkerold[(shape-1)/2])	 
    current_angle = len(indiceold)/2 * scan.angle_increment
    return (indiceold)

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
