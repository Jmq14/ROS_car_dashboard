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

class Ui_MainWindow(QtCore.QObject):

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

        # self.connect(self.reader, QtCore.SIGNAL("left_img_timestamp"),
        #         self.update_left_timestamp)
        # self.connect(self.reader, QtCore.SIGNAL("right_img_timestamp"),
        #         self.update_right_timestamp)
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
        #self.lidar_graphicsView.clear_readings()
        #for x, y, z, intensity, ring in point_cloud2.read_points( data ):
        #    temp = [x, y, z, intensity, ring, 0, 0]
        #    self.lidar_graphicsView.load_reading(temp)

        #self.lidar_graphicsView.update()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1172, 860)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.time_label = QtGui.QLabel(self.centralWidget)
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.horizontalLayout_3.addWidget(self.time_label)
        self.time_display = QtGui.QLabel(self.centralWidget)
        self.time_display.setMinimumSize(QtCore.QSize(100, 0))
        self.time_display.setText(_fromUtf8(""))
        self.time_display.setObjectName(_fromUtf8("time_display"))
        self.horizontalLayout_3.addWidget(self.time_display)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.left_img = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_img.sizePolicy().hasHeightForWidth())
        self.left_img.setSizePolicy(sizePolicy)
        self.left_img.setMinimumSize(QtCore.QSize(320, 320))
        self.left_img.setText(_fromUtf8(""))
        self.left_img.setTextFormat(QtCore.Qt.AutoText)
        self.left_img.setObjectName(_fromUtf8("left_img"))
        self.verticalLayout.addWidget(self.left_img)
        self.left_label = QtGui.QLabel(self.centralWidget)
        self.left_label.setObjectName(_fromUtf8("left_label"))
        self.verticalLayout.addWidget(self.left_label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.right_img = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_img.sizePolicy().hasHeightForWidth())
        self.right_img.setSizePolicy(sizePolicy)
        self.right_img.setMinimumSize(QtCore.QSize(320, 320))
        self.right_img.setText(_fromUtf8(""))
        self.right_img.setTextFormat(QtCore.Qt.AutoText)
        self.right_img.setObjectName(_fromUtf8("right_img"))
        self.verticalLayout_2.addWidget(self.right_img)
        self.right_label = QtGui.QLabel(self.centralWidget)
        self.right_label.setObjectName(_fromUtf8("right_label"))
        self.verticalLayout_2.addWidget(self.right_label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lidar_graphicsView = LIDARVisualizer(self.centralWidget) 
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lidar_graphicsView.sizePolicy().hasHeightForWidth())
        self.lidar_graphicsView.setSizePolicy(sizePolicy)
        self.lidar_graphicsView.setMinimumSize(QtCore.QSize(400, 320))
        self.lidar_graphicsView.setObjectName(_fromUtf8("lidar_graphicsView"))
        self.verticalLayout_3.addWidget(self.lidar_graphicsView)
        self.lidar_label = QtGui.QLabel(self.centralWidget)
        self.lidar_label.setObjectName(_fromUtf8("lidar_label"))
        self.verticalLayout_3.addWidget(self.lidar_label)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setMargin(11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.velocity_label = QtGui.QLabel(self.centralWidget)
        self.velocity_label.setObjectName(_fromUtf8("velocity_label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.velocity_label)
        self.velocity_textEdit = QtGui.QTextEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.velocity_textEdit.sizePolicy().hasHeightForWidth())
        self.velocity_textEdit.setSizePolicy(sizePolicy)
        self.velocity_textEdit.setReadOnly(True)
        self.velocity_textEdit.setObjectName(_fromUtf8("velocity_textEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.velocity_textEdit)
        self.angle_label = QtGui.QLabel(self.centralWidget)
        self.angle_label.setObjectName(_fromUtf8("angle_label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.angle_label)
        self.angle_textEdit = QtGui.QTextEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.angle_textEdit.sizePolicy().hasHeightForWidth())
        self.angle_textEdit.setSizePolicy(sizePolicy)
        self.angle_textEdit.setReadOnly(True)
        self.angle_textEdit.setObjectName(_fromUtf8("angle_textEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.angle_textEdit)
        self.gear_label = QtGui.QLabel(self.centralWidget)
        self.gear_label.setObjectName(_fromUtf8("gear_label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.gear_label)
        self.gear_textEdit = QtGui.QTextEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gear_textEdit.sizePolicy().hasHeightForWidth())
        self.gear_textEdit.setSizePolicy(sizePolicy)
        self.gear_textEdit.setReadOnly(True)
        self.gear_textEdit.setObjectName(_fromUtf8("gear_textEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.gear_textEdit)
        self.brake_label = QtGui.QLabel(self.centralWidget)
        self.brake_label.setObjectName(_fromUtf8("brake_label"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.brake_label)
        self.brake_textEdit = QtGui.QTextEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brake_textEdit.sizePolicy().hasHeightForWidth())
        self.brake_textEdit.setSizePolicy(sizePolicy)
        self.brake_textEdit.setReadOnly(True)
        self.brake_textEdit.setObjectName(_fromUtf8("brake_textEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.brake_textEdit)
        self.throttle_label = QtGui.QLabel(self.centralWidget)
        self.throttle_label.setObjectName(_fromUtf8("throttle_label"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.throttle_label)
        self.throttle_textEdit = QtGui.QTextEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.throttle_textEdit.sizePolicy().hasHeightForWidth())
        self.throttle_textEdit.setSizePolicy(sizePolicy)
        self.throttle_textEdit.setReadOnly(True)
        self.throttle_textEdit.setObjectName(_fromUtf8("throttle_textEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.throttle_textEdit)
        self.horizontalLayout_2.addLayout(self.formLayout)

        rospack = rospkg.RosPack()
        pwd = rospack.get_path('monitor') 
        self.webView = QtWebKit.QWebView(self.centralWidget)
        self.webView.load(QtCore.QUrl.fromLocalFile(
            _fromUtf8(os.path.join(pwd, "src/QtWeb/velocity.html"))))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout_2.addWidget(self.webView)
        self.webView_map = QtWebKit.QWebView(self.centralWidget)
        self.webView_map.load(QtCore.QUrl.fromLocalFile(
            _fromUtf8(os.path.join(pwd, "src/QtWeb/map.html"))))
        self.webView_map.setObjectName(_fromUtf8("webView_map"))
        self.horizontalLayout_2.addWidget(self.webView_map)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1172, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.left_label.setText(_translate("MainWindow", "Left camera", None))
        self.right_label.setText(_translate("MainWindow", "Right camera", None))
        self.velocity_label.setText(_translate("MainWindow", "Velocity", None))
        self.gear_label.setText(_translate("MainWindow", "Gear", None))
        self.brake_label.setText(_translate("MainWindow", "Brake pedal", None))
        self.throttle_label.setText(_translate("MainWindow", "Throttle pedal", None))
        self.angle_label.setText(_translate("MainWindow", "Angle", None))
        self.time_label.setText(_translate("MainWindow", "ROS time", None))
        self.lidar_label.setText(_translate("MainWindow", "Lidar", None))

