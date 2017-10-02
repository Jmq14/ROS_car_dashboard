# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/parallels/Desktop/monitor/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import cv2
import numpy as np

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
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        self.brake_display(self.reader.brake)
        self.throttle_display(self.reader.throttle)
#        self.left_img_display(self.reader.left_img, self.reader.left_time)
#        self.right_img_display(self.reader.right_img)
        self.steering_display(self.reader.steering)
        self.gear_display(self.reader.gear)

    def brake_display(self, data):
        self.brake_textEdit.setText(data)
        a = int(float(data) * 100)
        self.brake_slider.setValue(a)

    def throttle_display(self, data):
        self.throttle_textEdit.setText(data)
        a = int(float(data) * 100)
        self.throttle_slider.setValue(a)

    def steering_display(self, data):
        self.angle_textEdit.setText(str(data.steering_wheel_angle))
        self.velocity_textEdit.setText(str(data.speed))
#        print "steering display " + str(data.header.stamp)

    def gear_display(self, data):
        self.gear_textEdit.setText(data)

    def left_img_display(self, cv_image, time):
        height, width, channel = cv_image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(cv_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        qPix = QtGui.QPixmap.fromImage(qImg)
        self.left_img.setPixmap(qPix)
 #       print "left img display " + time

    def right_img_display(self, cv_image):
        # if self.right_stamp < self.steer_stamp: pass
        height, width, channel = cv_image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(cv_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        qPix = QtGui.QPixmap.fromImage(qImg)
        self.right_img.setPixmap(qPix)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(720, 720)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.left_img = QtGui.QLabel(self.centralWidget)
        self.left_img.setGeometry(QtCore.QRect(20, 20, 320, 320))
        self.left_img.setText(_fromUtf8(""))
        self.left_img.setTextFormat(QtCore.Qt.AutoText)
        self.left_img.setObjectName(_fromUtf8("left_img"))
        self.right_img = QtGui.QLabel(self.centralWidget)
        self.right_img.setGeometry(QtCore.QRect(360, 20, 320, 320))
        self.right_img.setText(_fromUtf8(""))
        self.right_img.setTextFormat(QtCore.Qt.AutoText)
        self.right_img.setObjectName(_fromUtf8("right_img"))
        self.left_label = QtGui.QLabel(self.centralWidget)
        self.left_label.setGeometry(QtCore.QRect(120, 350, 101, 31))
        self.left_label.setObjectName(_fromUtf8("left_label"))
        self.right_label = QtGui.QLabel(self.centralWidget)
        self.right_label.setGeometry(QtCore.QRect(480, 350, 111, 31))
        self.right_label.setObjectName(_fromUtf8("right_label"))
        self.velocity_label = QtGui.QLabel(self.centralWidget)
        self.velocity_label.setGeometry(QtCore.QRect(70, 440, 67, 17))
        self.velocity_label.setObjectName(_fromUtf8("velocity_label"))
        self.gear_label = QtGui.QLabel(self.centralWidget)
        self.gear_label.setGeometry(QtCore.QRect(70, 520, 67, 17))
        self.gear_label.setObjectName(_fromUtf8("gear_label"))
        self.gear_textEdit =  QtGui.QTextEdit(self.centralWidget)
        self.gear_textEdit.setGeometry(QtCore.QRect(140, 520, 120, 31))
        self.gear_textEdit.setReadOnly(True)
        self.gear_textEdit.setObjectName(_fromUtf8("gear_textEdit"))
        self.brake_label = QtGui.QLabel(self.centralWidget)
        self.brake_label.setGeometry(QtCore.QRect(290, 440, 101, 17))
        self.brake_label.setObjectName(_fromUtf8("brake_label"))
        self.throttle_label = QtGui.QLabel(self.centralWidget)
        self.throttle_label.setGeometry(QtCore.QRect(290, 480, 111, 17))
        self.throttle_label.setObjectName(_fromUtf8("throttle_label"))
        self.angle_label = QtGui.QLabel(self.centralWidget)
        self.angle_label.setGeometry(QtCore.QRect(70, 480, 67, 17))
        self.angle_label.setObjectName(_fromUtf8("angle_label"))
        self.brake_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.brake_textEdit.setGeometry(QtCore.QRect(400, 430, 140, 31))
        self.brake_textEdit.setReadOnly(True)
        self.brake_textEdit.setObjectName(_fromUtf8("brake_textEdit"))
        self.throttle_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.throttle_textEdit.setGeometry(QtCore.QRect(400, 470, 140, 31))
        self.throttle_textEdit.setReadOnly(True)
        self.throttle_textEdit.setObjectName(_fromUtf8("throttle_textEdit"))
        self.angle_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.angle_textEdit.setGeometry(QtCore.QRect(140, 470, 140, 31))
        self.angle_textEdit.setReadOnly(True)
        self.angle_textEdit.setObjectName(_fromUtf8("angle_textEdit"))
        self.velocity_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.velocity_textEdit.setGeometry(QtCore.QRect(140, 430, 140, 31))
        self.velocity_textEdit.setReadOnly(True)
        self.velocity_textEdit.setObjectName(_fromUtf8("velocity_textEdit"))
        self.brake_slider = QtGui.QSlider(self.centralWidget)
        self.brake_slider.setGeometry(QtCore.QRect(560, 440, 101, 16))
        self.brake_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brake_slider.setObjectName(_fromUtf8("brake_slider"))
        self.brake_slider.setRange(15, 50)
        self.throttle_slider = QtGui.QSlider(self.centralWidget)
        self.throttle_slider.setGeometry(QtCore.QRect(560, 480, 101, 16))
        self.throttle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.throttle_slider.setObjectName(_fromUtf8("throttle_slider"))
        self.throttle_slider.setRange(15, 50)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 720, 22))
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

