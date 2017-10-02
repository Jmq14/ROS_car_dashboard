#!/usr/bin/env python

import cv2
import os
import thread, time
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError

from std_msgs.msg import *
from sensor_msgs.msg import *
from dbw_mkz_msgs.msg import *
from geometry_msgs.msg import Twist

class Reporter():

    def __init__(self):
        
        self.time = 0
        self.left_camera  = 0 
        self.right_camera = 0
        self.brake        = None 
        self.throttle     = None
        self.gear         = 0
        self.speed        = 0
        self.angle        = 0
        self.steer        = 0
        self.wheel_speed  = 0
        self.velocity     = 0
        self.dbw_enabled  = False
        self.cmd_vel      =  None

        thread.start_new_thread(self.monitor_print,())

    def monitor_print(self):
        while True:
            time.sleep(0.1)
            rospy.loginfo('''
 dbw enabled     : {}
 cmd vel         : 
 {}
 brake cmd       : {} (0.15-5.0)
 throttle cmd    : {} (0.15-5.0)
 wheel speed     : {} rad/s
 wheel angle     : {} rad
'''.format(self.dbw_enabled, self.cmd_vel, self.brake, 
    self.throttle, self.speed, self.angle))


class Reader():

    def __init__(self):
        
        rospy.init_node('monitor', anonymous=True) 
        rospy.loginfo('init reader')

        self.left_camera  = '/left_camera/pg_16492265/image_color_flipped/compressed'
        self.right_camera = '/right_camera/pg_16492281/image_color_flipped/compressed'
        self.brake        = '/vehicle/brake_cmd'
        self.throttle     = '/vehicle/throttle_cmd'
        self.gear         = '/vehicle/gear_report'
        self.steer        = '/vehicle/steering_cmd'
        self.wheel_speed  = '/vehicle/wheel_speed_report'
        self.dbw_enabled  = '/vehicle/dbw_enabled'
        self.cmd_vel      = '/vehicle/cmd_vel'

        self.reporter = Reporter()

        rospy.Subscriber(self.left_camera, 
                CompressedImage, self.left_camera_sender)

        rospy.Subscriber(self.right_camera, 
                CompressedImage, self.right_camera_sender)

        rospy.Subscriber(self.brake, 
                BrakeReport, self.brake_sender)
        
        rospy.Subscriber(self.throttle, 
                ThrottleReport, self.throttle_sender)

        rospy.Subscriber(self.gear, 
                GearReport, self.gear_sender)

        rospy.Subscriber(self.steer, 
                SteeringReport, self.steer_sender)

        rospy.Subscriber(self.wheel_speed, 
                WheelSpeedReport, self.wheel_speed_sender)

        rospy.Subscriber(self.dbw_enabled,
                Bool, self.dbw_enabled_sender)

        rospy.Subscriber(self.cmd_vel, 
                Twist, self.cmd_vel_sender)

        rospy.spin()

    def left_camera_sender(self, data):
        # data
        pass

    def right_camera_sender(self, data):
        # data
        pass

    def brake_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        # self.reporter.brake = data.pedal_cmd
        self.reporter.brake = data

    def throttle_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        # self.reporter.throttle = data.pedal_cmd
        self.reporter.throttle = data

    def gear_sender(self, data):
        # state
        # uint8 NONE=0
        # uint8 PARK=1
        # uint8 REVERSE=2
        # uint8 NEUTRAL=3
        # uint8 DRIVE=4
        # uint8 LOW=5
        # self.reporter.gear = data.state.gear
        pass

    def steer_sender(self, data):
        # float32 steering_wheel_angle_cmd        # rad, range -8.2 to 8.2
        # float32 steering_wheel_angle_velocity   # rad/s, range 0 to 8.7, 0 = maximum

        # # Steering Wheel
        # float32 steering_wheel_angle      # rad
        # float32 steering_wheel_angle_cmd  # rad
        # float32 steering_wheel_torque     # Nm

        # # Vehicle Speed
        # float32 speed                     # m/s
        self.reporter.speed = data.steering_wheel_angle_velocity
        self.reporter.angle = data.steering_wheel_angle_cmd

    def wheel_speed_sender(self, data):
        # # Wheel speeds (rad/s)
        # float32 front_left
        # float32 front_right
        # float32 rear_left
        # float32 rear_right
        # self.reporter.speed = data.front_left
        pass

    def dbw_enabled_sender(self, data):
        self.reporter.dbw_enabled = data.data

    def cmd_vel_sender(self, data):
        self.reporter.cmd_vel = data

if __name__ == "__main__":
    import sys

    reader = Reader()

