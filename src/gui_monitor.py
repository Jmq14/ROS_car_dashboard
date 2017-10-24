# -*- coding: utf-8 -*-

from LIDARVisualizer import *
from PyQt4 import QtCore, QtGui, QtWebKit
import os, cv2
import numpy as np
import rospkg
from sensor_msgs import point_cloud2
import struct

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QWidget):

    def setupReader(self, reader):
        self.reader = reader
        self.connect(self.reader, QtCore.SIGNAL("gear"), 
                self.gear_textEdit.setText)
        self.connect(self.reader, QtCore.SIGNAL("brake_pedal"), 
                self.brake_display)
        self.connect(self.reader, QtCore.SIGNAL("throttle_pedal"), 
                self.throttle_display)
        self.connect(self.reader, QtCore.SIGNAL("angle"), 
                self.angle_textEdit.setText)
        self.connect(self.reader, QtCore.SIGNAL("velocity"), 
                self.velocity_display)
        self.connect(self.reader, QtCore.SIGNAL("left_img"),
               self.left_img_display)
        self.connect(self.reader, QtCore.SIGNAL("right_img"),
               self.right_img_display)
        self.connect(self.reader, QtCore.SIGNAL("gps"),
                self.gps_display)
        self.connect(self.reader, QtCore.SIGNAL("lidar"),
               self.lidar_display)
        self.connect(self.reader, QtCore.SIGNAL("time"),
                self.time_display.setText)

        self.connect(self.reader, QtCore.SIGNAL("steer_timestamp"),
                self.update_steer_timestamp)

        self.left_stamp = self.right_stamp = self.steer_stamp = None
        self.cnt = 0

    def update_left_timestamp(self, time):
        self.left_stamp = time
        print 'left img received ' + str(time)

    def update_right_timestamp(self, time): self.right_stamp = time
    def update_steer_timestamp(self, time): self.steer_stamp = time

    def brake_display(self, data):
        self.brake_textEdit.setText(data)
        a = int(float(data) * 100)
        #self.brake_slider.setValue(a)

    def throttle_display(self, data):
        self.throttle_textEdit.setText(data)
        a = int(float(data) * 100)
        #self.throttle_slider.setValue(a)

    def left_img_display(self, cv_image):
       #  if str(data.header.stamp) < self.steer_stamp: pass
        # print 'left img display ' + str(data.header.stamp)
        
    	height = self.left_img.height()
    	width  = self.left_img.width()
    	size = min(height, width)
    	cv_image = cv2.resize(cv_image, (size, size))

        bytesPerLine = 3 * size
        qImg = QtGui.QImage(cv_image.data, size, size, bytesPerLine, QtGui.QImage.Format_RGB888)
        qPix = QtGui.QPixmap.fromImage(qImg)
        self.left_img.setPixmap(qPix)

    def right_img_display(self, cv_image):
        # if self.right_stamp < self.steer_stamp: pass
    	height = self.right_img.height()
    	width  = self.right_img.width()
    	size = min(height, width)
    	cv_image = cv2.resize(cv_image, (size, size))

        bytesPerLine = 3 * size
        qImg = QtGui.QImage(cv_image.data, size, size, bytesPerLine, QtGui.QImage.Format_RGB888)
        qPix = QtGui.QPixmap.fromImage(qImg)
        self.right_img.setPixmap(qPix)

    def gps_display(self, gps):
        gps_info = gps.split(' ')
        status = gps_info[0]
        latitude = gps_info[1]
        longitude = gps_info[2]
        self.webView_map.page().mainFrame().evaluateJavaScript(
                "updateLocation({}, {})".format(latitude, longitude))

    def velocity_display(self, v):
        self.velocity_textEdit.setText(v)
        self.cnt += 1
        if not self.cnt % 10 == 0:
            return
        self.cnt = 0
        self.webView.page().mainFrame().evaluateJavaScript(
                "new_velocity({}, {})".format(self.steer_stamp, v))

    def lidar_display(self, data):
        self.lidar_graphicsView.load_xyzi_pc_and_render(data.data)

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        size = min(width, height)
        
        self.lidar_graphicsView.setGeometry(0, 0, width * 2 / 3.0, height * 2 / 3.0)
        self.lidar_graphicsView.move(0, 0)

        self.time_display.move(0,0)
        self.time_display.raise_()
        
        self.right_img.move(2 * width / 3.0, 0)
        self.right_img.resize(width / 3.0, width / 3.0)
        self.left_img.move(2 * width / 3.0, width / 3.0)
        self.left_img.resize(width / 3.0, width / 3.0)


        self.webView_map.move(0, 2 * height / 3.0)
        self.webView_map.resize(height / 3.0, height / 3.0)

        self.webView.move(height / 3.0, 2 * height / 3.0)
        self.webView.resize(height / 3.0, height / 3.0)

        self.info.move(2 * height / 3.0, 2 * height / 3.0)
        self.info.resize(height / 3.0, height / 3.0)

    def setupUi(self):
        self.time_display = QtGui.QLabel(self)
        self.time_display.setMinimumSize(QtCore.QSize(100, 0))
        self.time_display.setText(_fromUtf8(""))
        self.time_display.setObjectName(_fromUtf8("time_display"))
        self.time_display.setStyleSheet("color: white")

        self.left_img = QtGui.QLabel(self)
        self.left_img.setObjectName(_fromUtf8("left_img"))

        self.right_img = QtGui.QLabel(self)
        self.right_img.setObjectName(_fromUtf8("right_img"))

        self.lidar_graphicsView = LIDARVisualizer(self) 
        self.lidar_graphicsView.setMinimumSize(QtCore.QSize(400, 320))
        self.lidar_graphicsView.setObjectName(_fromUtf8("lidar_graphicsView"))
        
        self.info = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.info.setLayout(self.gridLayout)

        self.velocity_label = QtGui.QLabel(self.info)
        self.velocity_label.setObjectName(_fromUtf8("velocity_label"))
        self.gridLayout.addWidget(self.velocity_label, 0, 0)

        self.velocity_textEdit = QtGui.QTextEdit(self.info)
        self.velocity_textEdit.setReadOnly(True)
        self.velocity_textEdit.setObjectName(_fromUtf8("velocity_textEdit"))

        self.gridLayout.addWidget(self.velocity_textEdit, 0, 1)

        self.angle_label = QtGui.QLabel(self.info)
        self.angle_label.setObjectName(_fromUtf8("angle_label"))

        self.gridLayout.addWidget(self.angle_label, 1, 0)

        self.angle_textEdit = QtGui.QTextEdit(self.info)
        self.angle_textEdit.setReadOnly(True)
        self.angle_textEdit.setObjectName(_fromUtf8("angle_textEdit"))

        self.gridLayout.addWidget(self.angle_textEdit, 1, 1)

        self.gear_label = QtGui.QLabel(self.info)
        self.gear_label.setObjectName(_fromUtf8("gear_label"))

        self.gridLayout.addWidget(self.gear_label, 2, 0)

        self.gear_textEdit = QtGui.QTextEdit(self.info)
        self.gear_textEdit.setReadOnly(True)
        self.gear_textEdit.setObjectName(_fromUtf8("gear_textEdit"))

        self.gridLayout.addWidget(self.gear_textEdit, 2, 1)

        self.brake_label = QtGui.QLabel(self.info)
        self.brake_label.setObjectName(_fromUtf8("brake_label"))

        self.gridLayout.addWidget(self.brake_label, 3, 0)

        self.brake_textEdit = QtGui.QTextEdit(self.info)
        self.brake_textEdit.setReadOnly(True)
        self.brake_textEdit.setObjectName(_fromUtf8("brake_textEdit"))

        self.gridLayout.addWidget(self.brake_textEdit, 3, 1)

        self.throttle_label = QtGui.QLabel(self.info)
        self.throttle_label.setObjectName(_fromUtf8("throttle_label"))

        self.gridLayout.addWidget(self.throttle_label, 4, 0)

        self.throttle_textEdit = QtGui.QTextEdit(self.info)
        self.throttle_textEdit.setReadOnly(True)
        self.throttle_textEdit.setObjectName(_fromUtf8("throttle_textEdit"))

        self.gridLayout.addWidget(self.throttle_textEdit, 4, 1)

        self.velocity_label.setText("Velocity")
        self.gear_label.setText("Gear")
        self.brake_label.setText("Brake pedal")
        self.throttle_label.setText("Throttle pedal")
        self.angle_label.setText("Angle")

        rospack = rospkg.RosPack()
        pwd = rospack.get_path('monitor') 
        self.webView = QtWebKit.QWebView(self)
        self.webView.load(QtCore.QUrl.fromLocalFile(
            _fromUtf8(os.path.join(pwd, "src/QtWeb/velocity.html"))))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.webView_map = QtWebKit.QWebView(self)
        self.webView_map.load(QtCore.QUrl.fromLocalFile(
            _fromUtf8(os.path.join(pwd, "src/QtWeb/map.html"))))
        self.webView_map.setObjectName(_fromUtf8("webView_map"))

        QtCore.QMetaObject.connectSlotsByName(self)

