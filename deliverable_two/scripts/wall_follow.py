#!/usr/bin/env python

from __future__ import print_function
from numpy import mean
import rospy
import std_msgs.msg
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sys
import time

rospy.init_node("teleop_robot")
pub = rospy.Publisher("/triton_lidar/vel_cmd", Twist, queue_size=10)
rate = rospy.Rate(10)
up = 0
left = 0
down = 0
right = 0

def callback(data):
    global up
    global down
    global left
    global right

    for curr in data.ranges:
        if(curr < data.range_min):
            curr = data.range_min
        elif(curr > data.range_max):
            curr = data.range_max

    up = ( sum(data.ranges[0:45]) + sum(data.ranges[315:360]) ) / 9.0
    left = sum(data.ranges[45:135]) / 9.0
    down = sum(data.ranges[135:225]) / 9.0
    right = sum(data.ranges[225:315]) / 9.0

    #rospy.loginfo(rospy.get_caller_id() + "I heard")
    #print("up:", up, "left:", left, "right:", right, "down:", down)
    
subscriber = rospy.Subscriber("/scan", LaserScan, callback)

msg = Twist()

while not rospy.is_shutdown():
    global msg
    global pub

    print("up:", up, "left:", left, "right:", right, "down:", down)
    
    closest = min([up, down, left, right])
    if(closest > 3.0):
        if(up == closest):
            msg.linear.x = 0.1
#            print("Moving UP!")
        elif(down == closest):
            msg.linear.x = -0.1
#            print("Moving DOWN!")
        elif(right == closest):
            msg.linear.y = -0.1
#            print("Moving RIGHT!")
        elif(left == closest):
            msg.linear.y = 0.1
#            print("Moving LEFT!")
    if(up < 3.0 and down < 3.0 and left < 3.0 and right < 3.0):
        msg = Twist()
    if(up < 2.0):
        msg.linear.x = -0.1
#        print("DOWN")
    if(down < 2.0):
        msg.linear.x = 0.1
#        print("UP")
    if(left < 2.0):
        msg.linear.y = -0.1
#        print("RIGHT")
    if(right < 2.0):
        msg.linear.y = 0.1
#        print("LEFT")
    
    if(2.0 < up < 3.0):
        msg.linear.y = -0.2
    if(2.0 < right < 3.0):
        msg.linear.x = -0.2
    if(2.0 < down < 3.0):
        msg.linear.y = 0.2
    if(2.0 < left < 3.0):
        msg.linear.x = 0.2

    rate.sleep()
    pub.publish(msg)
    rate.sleep()
