#!/usr/bin/env python
# Author: David Shearon 2/15/23

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=False)
    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish('[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]')
        
        deg_to_rad = 0.01745329252 
        msg = Twist()
      

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 135 
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)
        
        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 135
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)
        
        msg.linear.x = 3
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 135
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 3
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.5
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.5
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 1.2
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.5
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.25
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 3.2
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.25
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.8
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 1
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -45
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 2.9
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)
######################
        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 2.9 
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -45
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 1
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.8
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.25
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 3.2
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.25
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.5
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 1.2
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)
        
        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.5
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * -90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0.4
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 90
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 3
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 135
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 3.2
        msg.angular.z = deg_to_rad * 0
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        msg.linear.x = 0
        msg.angular.z = deg_to_rad * 135
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo(msg)

        break

if __name__ == '__main__':
    global msg
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
