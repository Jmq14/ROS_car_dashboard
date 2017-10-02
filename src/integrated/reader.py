#!/usr/bin/env python

import cv2
import os
import numpy as np
import rospy
from PyQt4 import QtGui, QtCore
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import *
from dbw_mkz_msgs.msg import *

from gui_monitor import Ui_MainWindow

class Reader(QtCore.QObject):

    def __init__(self, parent=None):

        super(Reader, self).__init__(parent)
        
        rospy.init_node('monitor', anonymous=True) 
        rospy.loginfo('init reader')

        self.left_camera_name  = '/left_camera/pg_16492265/image_color_flipped/compressed'
        self.right_camera_name = '/right_camera/pg_16492281/image_color_flipped/compressed'
        self.compressed = True

        self.brake_name        = '/vehicle/brake_report'
        self.throttle_name     = '/vehicle/throttle_report'
        self.gear_name         = '/vehicle/gear_report'
        self.steer_name        = '/vehicle/steering_report'
        self.wheel_speed_name  = '/vehicle/wheel_speed_report'

        # control fps
        self.left_frame_count = 0
        self.right_frame_count = 0

        # msg -> image converter
        self.bridge = CvBridge()

        # reports
        self.brake = self.throttle = self.gear = self.steering = self.left_img = self.right_img = None

    def setup_subscriber(self):

        rospy.Subscriber(self.left_camera_name, 
                CompressedImage, self.left_camera_sender)

        rospy.Subscriber(self.right_camera_name, 
                CompressedImage, self.right_camera_sender)

        rospy.Subscriber(self.brake_name, 
                BrakeReport, self.brake_sender)
        
        rospy.Subscriber(self.throttle_name, 
                ThrottleReport, self.throttle_sender)

        rospy.Subscriber(self.gear_name, 
                GearReport, self.gear_sender)

        rospy.Subscriber(self.steer_name, 
                SteeringReport, self.steer_sender)

        rospy.Subscriber(self.wheel_speed_name, 
                WheelSpeedReport, self.wheel_speed_sender)

        rospy.spin()

    def left_camera_sender(self, data):
        # data

        # self.left_frame_count += 1
        # if self.left_frame_count % 2 == 0:
        #     self.left_frame_count = 0
        #     return

        print "new left img " + str(data.header.stamp.secs)

        if self.compressed:
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, 1)
        else:
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv_image = cv2.resize(cv_image, (320, 320))

        self.left_img = cv_image
        self.left_time = str(data.header.stamp)
        print "left img updated " + str(data.header.stamp.secs)

    def right_camera_sender(self, data):
        # data

        # self.right_frame_count += 1
        # if self.right_frame_count % 2 == 0:
        #     self.right_frame_count = 0
        #     return

        if self.compressed:
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, 1)
        else:
            cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv_image = cv2.resize(cv_image, (320, 320))

        self.right_img = cv_image

    def brake_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        self.brake = str(data.pedal_output)

    def throttle_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        self.throttle = str(data.pedal_output)
        

    def gear_sender(self, data):
        # state
        # uint8 NONE=0
        # uint8 PARK=1
        # uint8 REVERSE=2
        # uint8 NEUTRAL=3
        # uint8 DRIVE=4
        # uint8 LOW=5
        state_num = int(data.state.gear)
        states = ['None', 'Park', 'Reverse', 'Neutral', 'Drive', 'Low']
        self.gear = states[state_num]

    def steer_sender(self, data):
        # float32 steering_wheel_angle_cmd        # rad, range -8.2 to 8.2
        # float32 steering_wheel_angle_velocity   # rad/s, range 0 to 8.7, 0 = maximum

        # # Steering Wheel
        # float32 steering_wheel_angle      # rad
        # float32 steering_wheel_angle_cmd  # rad
        # float32 steering_wheel_torque     # Nm

        # # Vehicle Speed
        # float32 speed                     # m/s
        self.steering = data
        print "steering updated " + str(data.header.stamp.secs)

    def wheel_speed_sender(self, data):
        # # Wheel speeds (rad/s)
        # float32 front_left
        # float32 front_right
        # float32 rear_left
        # float32 rear_right
        pass

