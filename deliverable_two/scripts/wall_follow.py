#!/usr/bin/env python

from __future__ import print_function
from numpy import mean
import random
import rospy
import std_msgs.msg
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
import sys
import time
from gazebo_msgs.srv import GetModelState
import numpy as np
from std_srvs.srv import Empty
import math
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.srv import SetModelState

rospy.init_node("teleop_robot")
pub = rospy.Publisher("/triton_lidar/vel_cmd", Twist, queue_size=10)
rate = rospy.Rate(2)
up = 0
left = 0
right = 0
upRight = 0

terminal_count = 0
last_coord_x = 0
last_coord_y = 0

def get_combo(LEFT, FRONT, FRONT_RIGHT, RIGHT):
    combo_string = ""
    combo_index = 0
    if(LEFT < 0.3):
        combo_index += 0
    else:
        combo_index += 1
    if(FRONT < 0.6):
        combo_index += 0
    elif(FRONT < 0.7):
        combo_index += 5
    elif(FRONT < 1.25):
        combo_index += 10
    else:
        combo_index += 15
    if(FRONT_RIGHT < 1.25):
        combo_index += 0
    else:
        combo_index += 25
    if(RIGHT < 0.3):
        combo_index += 0
    elif(RIGHT < 0.45):
        combo_index += 125
    elif(RIGHT < 0.6):
        combo_index += 250
    elif(RIGHT < 0.8):
        combo_index += 375
    else:
        combo_index += 500
    return combo_index

def check_terminal():
    rospy.wait_for_service('/gazebo/get_model_state')
    x = 0
    y = 0
    z = 0
    global terminal_count
    global last_coord_x
    global last_coord_y
    global episode_count
    global right
    global up
    global left

    try:
        gms = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
        resp = gms("triton_lidar", "world")

        x = resp.pose.position.x
        y = resp.pose.position.y
        z = resp.pose.position.z
    except:
        print("error")

#    dist_from_last = math.dist([last_coord_x, last_coord_y], [x, y])
    dist_from_last = np.linalg.norm(np.array((last_coord_x, last_coord_y)) - np.array((x, y)))
   # print(dist_from_last)
    if(dist_from_last < 0.12):
        terminal_count += 1
    else:
        terminal_count = 0
        last_coord_x = x
        last_coord_y = y

    if(terminal_count >= 2 or z > 1):
        state_msg = ModelState()
        angle = float(random.random() * 6.28)
        state_msg.model_name = 'triton_lidar'
        state_msg.pose.position.x = 0
        state_msg.pose.position.y = 0
        state_msg.pose.position.z = 0
        state_msg.twist.angular.x = 0
        state_msg.pose.orientation.x = 0
        state_msg.pose.orientation.y = 0
        state_msg.pose.orientation.z = np.sin(angle/2)
        state_msg.pose.orientation.w = np.cos(angle/2)
        state_msg.twist.angular.y = 3.14
        state_msg.twist.angular.z = 3.14
       # print(angle)

        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state( state_msg )
        
       # reset_world = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
       # reset_world()
        episode_count += 1
        print("RESETTING!")
        return -5
    elif(right < 0.3 or left < 0.3 or up < 0.3 or right > 0.8):
        print("SHAME!")
        return -5
    print("GOOD BOY!")
    return 20

def callback(data):
    global up
    global upRight
    global left
    global right

    for curr in data.ranges:
        if(curr < data.range_min):
            curr = data.range_min
        elif(curr > data.range_max):
            curr = data.range_max

    right = ( sum(data.ranges[0:34]) + sum(data.ranges[326:360]) ) / 68.0
    left = sum(data.ranges[124:236]) / 112.0
    upRight = ( sum(data.ranges[0:57]) + sum(data.ranges[349:360]) )/ 68.0
    up = sum(data.ranges[56:124]) / 68.0

subscriber = rospy.Subscriber("/scan", LaserScan, callback)

msg = Twist()
q_table = np.zeros((542, 3))

epsilon_0 = 0.98
d = 0.9
episode_count = 0
epsilon = 0

rate.sleep()
rate.sleep()

while not rospy.is_shutdown():
    global msg
    global pub
    global q_table

    msg = Twist()

    r = random.random()
    epsilon = epsilon_0 * pow(d, episode_count)

    combo_index = get_combo(left, up, upRight, right)       # get index of current situation
    if(r < epsilon):
        #explore
        print("RANDOM", end='\t\t')
        action_index = random.randrange(3)                  # Choose random action
        learning_rate = 0.2
        discount_factor = 0.8

        if(action_index == 0):
        #    print("Turning Left!")
            msg.angular.z = -1
            msg.linear.y = 0.3
        elif(action_index == 2):
        #    print("Turning Right!")
            msg.angular.z = 1
            msg.linear.y = 0.3
        else:
        #    print("Going Straight!")
            msg.linear.y = 0.6

    else:
        #exploit
        print("COMPUTED", end='\t')
        max_option = max(q_table[combo_index, :])
        if(max_option == q_table[combo_index, 1]):
            #go straight
            print("Going Straight!")
            msg.linear.y = 0.6
        elif(max_option == q_table[combo_index, 0]):
            print("Turning Left!")
            msg.angular.z = -1
            msg.linear.y = 0.3
           #turn left
        elif(max_option == q_table[combo_index, 2]):
            #turn right
            print("Turning Right!")
            msg.angular.z = 1
            msg.linear.y = 0.3

        pub.publish(msg)
        try:
            rate.sleep()
        except:
            print("", end="")

        next_combo_index = get_combo(left, up, upRight, right)
        q_table[combo_index, action_index] = q_table[combo_index, action_index] + learning_rate * (check_terminal() + discount_factor * max(q_table[next_combo_index, :]) - q_table[combo_index, action_index])    
