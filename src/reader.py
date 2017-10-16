#!/usr/bin/env python

import cv2
import os
import numpy as np
import rospy
from PyQt4 import QtGui, QtCore
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import *
from dbw_mkz_msgs.msg import *
from nmea_msgs.msg import Sentence
from rosgraph_msgs.msg import Clock

from gui_monitor import Ui_MainWindow

class Reader(QtCore.QObject):

    def __init__(self, parent=None):

        super(Reader, self).__init__(parent)
        
        rospy.init_node('monitor', anonymous=True) 

        self.left_camera  = '/left_camera/pg_16492265/image_color_flipped/compressed'
        self.right_camera = '/right_camera/pg_16492281/image_color_flipped/compressed'
        self.compressed = True

        self.brake        = '/vehicle/brake_report'
        self.throttle     = '/vehicle/throttle_report'
        self.gear         = '/vehicle/gear_report'
        self.steer        = '/vehicle/steering_report'
        self.wheel_speed  = '/vehicle/wheel_speed_report'
        self.nmea_gps     = '/nmea_sentence'
        self.lidar        = '/velodyne_points'

    	self.clock        = '/clock'


        # control fps
        self.left_frame_count = 0
        self.right_frame_count = 0

        # msg -> image converter
        self.bridge = CvBridge()

    def setup_subscriber(self):

        rospy.Subscriber(self.left_camera, 
                Image, self.left_camera_sender, queue_size=3, buff_size=2**24)

        rospy.Subscriber(self.right_camera, 
                CompressedImage, self.right_camera_sender, queue_size=3, buff_size=2**24)

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

        rospy.Subscriber(self.nmea_gps,
                Sentence, self.nmea_gps_sender)

        rospy.Subscriber(self.lidar,
                PointCloud2, self.lidar_sender)

        rospy.Subscriber(self.clock, Clock, self.time_sender)

        rospy.spin()

    def left_camera_sender(self, data):
        # data

        if self.compressed:
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, 1)
        else:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        self.emit(QtCore.SIGNAL("left_img"), cv_image)
        self.emit(QtCore.SIGNAL("left_img_timestamp"), str(data.header.stamp))

    def right_camera_sender(self, data):
        # data

        if self.compressed:
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, 1)
        else:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        self.emit(QtCore.SIGNAL("right_img"), cv_image)
        self.emit(QtCore.SIGNAL("right_img_timestamp"), str(data.header.stamp))

    def brake_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        self.emit(QtCore.SIGNAL("brake_pedal"), str(data.pedal_output))

    def throttle_sender(self, data):
        # pedal_output
        # unitless, range 0.15 to 0.50
        self.emit(QtCore.SIGNAL("throttle_pedal"), str(data.pedal_output))

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
        self.emit(QtCore.SIGNAL("gear"), states[state_num])

    def steer_sender(self, data):
        # float32 steering_wheel_angle_cmd        # rad, range -8.2 to 8.2
        # float32 steering_wheel_angle_velocity   # rad/s, range 0 to 8.7, 0 = maximum

        # # Steering Wheel
        # float32 steering_wheel_angle      # rad
        # float32 steering_wheel_angle_cmd  # rad
        # float32 steering_wheel_torque     # Nm

        # # Vehicle Speed
        # float32 speed                     # m/s
        self.emit(QtCore.SIGNAL("angle"), str(data.steering_wheel_angle))
        self.emit(QtCore.SIGNAL("velocity"), str(data.speed))
        self.emit(QtCore.SIGNAL("steer_timestamp"), str(data.header.stamp))

    def wheel_speed_sender(self, data):
        # # Wheel speeds (rad/s)
        # float32 front_left
        # float32 front_right
        # float32 rear_left
        # float32 rear_right
        pass

    def nmea_gps_sender(self, data):

        s = data.sentence
        if s.startswith('<'): 
            info = s[1:].strip().split(' ')
            if info[0] == 'SOL_COMPUTED':
                status = info[1]
                latitude = float(info[2])
                longitude = float(info[3])
                altitude = float(info[4])
                
                accuracy = (float(info[7]), float(info[8]), float(info[9]))
                
                self.emit(QtCore.SIGNAL("gps"), 
                        "{} {} {}".format(status, latitude, longitude))

    def lidar_sender(self, data):
        self.emit(QtCore.SIGNAL("lidar"), data)

    def time_sender(self, data):
        clock = data.clock
        self.emit(QtCore.SIGNAL("time"), "%ds %d" % (clock.secs, clock.nsecs))

