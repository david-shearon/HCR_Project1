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
step_count = 0
terminal_count = 0
last_coord_x = 0
last_coord_y = 0
max_step = 0
episode_count = 0

# Produce a state index for use in the Q-Table
def get_combo(LEFT, FRONT, FRONT_RIGHT, RIGHT):
    combo_string = ""
    combo_index = 0
    if(LEFT < 0.6):
        combo_index += 0
    else:
        combo_index += 1
    if(FRONT < 0.6):
        combo_index += 0
    elif(FRONT < 0.7):
        combo_index += 5
    elif(FRONT < 1.0):
        combo_index += 10
    else:
        combo_index += 15
    if(FRONT_RIGHT < 1.2):
        combo_index += 0
    else:
        combo_index += 25
    if(RIGHT < 0.30):
        combo_index += 0
    elif(RIGHT < 0.4):
        combo_index += 125
    elif(RIGHT < 0.5):
        combo_index += 250
    elif(RIGHT < 0.6):
        combo_index += 375
    else:
        combo_index += 500
    return combo_index

# Check terminal cases, and produce reward
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
    global step_count

    try:
        gms = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
        resp = gms("triton_lidar", "world")

        x = resp.pose.position.x
        y = resp.pose.position.y
        z = resp.pose.position.z
    except:
        print("error")

    dist_from_last = np.linalg.norm(np.array((last_coord_x, last_coord_y)) - np.array((x, y)))

    # If robot trapped
    if(dist_from_last < 0.04):
        print("Robot Trapped!")
        terminal_count += 1
    else:
        terminal_count = 0
        last_coord_x = x
        last_coord_y = y

    # Check for reset and reset if needed
    if(terminal_count >= 2 or z > 1):
        print("Step count: ", step_count)
        np.savetxt("/q_table.csv", q_table, delimiter=",")
        step_count = 0
        state_msg = ModelState()
        angle = float(random.random() * 6.28)

        state_msg.model_name = 'triton_lidar'
        state_msg.pose.orientation.x = 0
        state_msg.pose.orientation.y = 0
        state_msg.pose.orientation.z = np.sin(angle/2)
        state_msg.pose.orientation.w = np.cos(angle/2)

        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state( state_msg )
        
        episode_count += 1
        print("RESETTING!")
        return -5
    elif(right < 0.20 or left < 0.6 or up < 0.3 or right > 0.7):
        print("SHAME!")
        return -5
    elif(terminal_count == 1):
        return -10
    print("GOOD BOY!")
    return 20

# Set range values from LiDAR
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

    right = ( sum(data.ranges[0:30]) + sum(data.ranges[330:360]) ) / 60.0
    left = sum(data.ranges[124:236]) / 112.0
    upRight = sum(data.ranges[30:70]) / 40.0
    up = sum(data.ranges[56:124]) / 68.0

subscriber = rospy.Subscriber("/scan", LaserScan, callback)

msg = Twist()
try:
    q_table = np.genfromtxt(fname = "/q_table.csv", delimiter = ',')
    print("Using saved q_table")
    print(np.shape(q_table))
    print(q_table)
except:
    print("Starting q_table from scratch!!")
    q_table = np.zeros((542, 3))

epsilon_0 = 0.98
d = 0.9
episode_count = 0
epsilon = 0
learning_rate = 0.2
discount_factor = 0.8

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
        action_index = random.randrange(3)                  # Choose random action

        if(action_index == 0):
            print("RANDOM!\t\tTurning Left!")
            msg.angular.z = 0.5
            msg.linear.y = 0.1
        elif(action_index == 2):
            print("RANDOM\t\tTurning Right!")
            msg.angular.z = -0.5
            msg.linear.y = 0.1
        else:
            print("RANDOM\t\tGoing Straight!")
            msg.linear.y = 0.4

    else:
        #exploit
        max_option = max(q_table[combo_index, :])
        if(max_option == q_table[combo_index, 1]):
            #go straight
            action_index = 1
            print("COMPUTED\tGoing Straight!")
            msg.linear.y = 0.4
        elif(max_option == q_table[combo_index, 0]):
            action_index = 0
            print("COMPUTED\tTurning Left!")
            msg.angular.z = 0.5
            msg.linear.y = 0.1
           #turn left
        elif(max_option == q_table[combo_index, 2]):
            #turn right
            action_index = 2
            print("COMPUTED\tTurning Right!")
            msg.angular.z = -0.5
            msg.linear.y = 0.1

    pub.publish(msg)
    try:
        rate.sleep()
    except:
        print("", end="")

    next_combo_index = get_combo(left, up, upRight, right)
    q_table[combo_index, action_index] = q_table[combo_index, action_index] + learning_rate * (check_terminal() + discount_factor * max(q_table[next_combo_index, :]) - q_table[combo_index, action_index])
    
    step_count += 1
    if(step_count > max_step):
        max_step = step_count
        print("New record! Max step is now: ", max_step)
        np.savetxt("/q_table.csv", q_table, delimiter=",")
