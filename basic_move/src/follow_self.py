#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point
from basic_move.msg import *
from aimbot.msg import DetectedRobot
from sensor_msgs.msg import LaserScan



pub = rospy.Publisher('/chassis_tomove', Move, queue_size = 100)
current_data = []
t_inc = 0
a_inc = 0
a_min = 0
a_max = 0
bot_size = 2
angle = 0
 #...in some units?
#assumes chassis and turret in same 'frame'
#data.type = enemy/ours...
#figure out how cv handles angles/where their 0 is
def robot_choice(self,data):
	angle = data.z_rotation
	dist = data.distance
	rot = room_to_move(angle,dist)
	whose = whoseBot(data)

	if whose:
		pub.publish(dist,angle,20,rot)
	else:
		print("shoot")
		#shooting?





def whoseBot(data):
	if data.type is 'enemy':
		return false
	else:
		return true

def room_to_move(angle,dist):
	start = angle/a_inc
	end = start + bot_size/a_inc
	farthest = move_pos(current_data[start:stop],a_inc)
	if((farthest(1[1]) != 0)):		
		return false
	elif (farthest(2)[1]*a_inc == self.angle):
		return false
	else:
		return true





   



def laser_handle(data):
	current_data = data.ranges
	a_max = data.angle_max
	a_min = data.angle_min
	t_inc = data.time_increment
	a_inc = data.angle_increment





def move_pos(scan,angle_increment):
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
    	stable = scan.ranges[0]
    	time+=1
    	current_angle = (scan.angle_increment*time)
        if scan.ranges[i] >= (stable)*.5:
            if(currentLength==0):
                checkernew = []
                indicenew = []
            currentLength+=1
            if currentLength > max:
                max = currentLength
            checkernew.append(item)
            indicenew.append(i)
        else:
            if(max==currentLength):
                checkerold = checkernew
                indiceold = indicenew
            currentLength = 0
            stable = scan.ranges[i]
    pos = 0
    shape = len(indiceold)
    if(shape > 0):
	    if(shape %2 ==0):
	    	pos = ((checkerold[shape/2]) + (checkerold[shape/2 - 1]))/2
	    else:
	    	pos = (checkerold[(shape-1)/2])	 
    current_angle = len(indiceold)/2 * scan.angle_increment
    return (checkerold,indiceold)


def listener():
    rospy.init_node('follow_self', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, laser_handle)
    ospy.Subscriber('/aimbot/detected_enemy',DetectedRobot,robot_choice)
    rospy.spin()