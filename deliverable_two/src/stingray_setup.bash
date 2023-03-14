#!/usr/bin/env bash

CATKIN_WS=~/Stingray-Simulation/catkin_ws

export GAZEBO_RESOURCE_PATH=$CATKIN_WS/src/stingray_sim
export GAZEBO_MODEL_PATH=$CATKIN_WS/src/stingray_sim/models
export GAZEBO_PLUGIN_PATH=$CATKIN_WS/devel/lib
