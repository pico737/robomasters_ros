 #!/usr/bin/env python
 
  import rospy
  from Move.msg import *
  
  
def talker():
    pub = rospy.Publisher('testp', Move , queue_size=10)
    rospy.init_node('quicktest', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        pub.publish(float(raw_input("roll")) , float(raw_input("pitch")) , float(raw_input("yaw")))
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
