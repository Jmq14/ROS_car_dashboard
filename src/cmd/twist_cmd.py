#!/usr/bin/env python

import rospy
from dbw_mkz_msgs.msg import *
from geometry_msgs.msg import *

def talker():
    pub = rospy.Publisher('/vehicle/cmd_vel', Twist, queue_size=10)
    rospy.init_node('monitor', anonymous=True)
    rate = rospy.Rate(20) # 10hz
    while not rospy.is_shutdown():
        twist_cmd = 
        pub.publish(twist_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
