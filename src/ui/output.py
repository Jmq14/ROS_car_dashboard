# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/nvidia/Desktop/monitor/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1159, 748)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.right_img = QtGui.QLabel(self.centralWidget)
        self.right_img.setGeometry(QtCore.QRect(360, 30, 320, 320))
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
        self.velocity_label.setGeometry(QtCore.QRect(70, 420, 61, 17))
        self.velocity_label.setObjectName(_fromUtf8("velocity_label"))
        self.gear_label = QtGui.QLabel(self.centralWidget)
        self.gear_label.setGeometry(QtCore.QRect(70, 500, 51, 17))
        self.gear_label.setObjectName(_fromUtf8("gear_label"))
        self.brake_label = QtGui.QLabel(self.centralWidget)
        self.brake_label.setGeometry(QtCore.QRect(40, 540, 71, 20))
        self.brake_label.setObjectName(_fromUtf8("brake_label"))
        self.throttle_label = QtGui.QLabel(self.centralWidget)
        self.throttle_label.setGeometry(QtCore.QRect(30, 580, 101, 20))
        self.throttle_label.setObjectName(_fromUtf8("throttle_label"))
        self.angle_label = QtGui.QLabel(self.centralWidget)
        self.angle_label.setGeometry(QtCore.QRect(70, 460, 51, 17))
        self.angle_label.setObjectName(_fromUtf8("angle_label"))
        self.brake_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.brake_textEdit.setGeometry(QtCore.QRect(130, 530, 131, 31))
        self.brake_textEdit.setReadOnly(True)
        self.brake_textEdit.setObjectName(_fromUtf8("brake_textEdit"))
        self.throttle_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.throttle_textEdit.setGeometry(QtCore.QRect(130, 570, 131, 31))
        self.throttle_textEdit.setReadOnly(True)
        self.throttle_textEdit.setObjectName(_fromUtf8("throttle_textEdit"))
        self.angle_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.angle_textEdit.setGeometry(QtCore.QRect(130, 450, 131, 31))
        self.angle_textEdit.setReadOnly(True)
        self.angle_textEdit.setObjectName(_fromUtf8("angle_textEdit"))
        self.velocity_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.velocity_textEdit.setGeometry(QtCore.QRect(130, 410, 131, 31))
        self.velocity_textEdit.setReadOnly(True)
        self.velocity_textEdit.setObjectName(_fromUtf8("velocity_textEdit"))
        self.gear_textEdit = QtGui.QTextEdit(self.centralWidget)
        self.gear_textEdit.setGeometry(QtCore.QRect(130, 490, 131, 31))
        self.gear_textEdit.setReadOnly(True)
        self.gear_textEdit.setObjectName(_fromUtf8("gear_textEdit"))
        self.time_label = QtGui.QLabel(self.centralWidget)
        self.time_label.setGeometry(QtCore.QRect(20, 0, 61, 20))
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.webView = QtWebKit.QWebView(self.centralWidget)
        self.webView.setGeometry(QtCore.QRect(290, 410, 400, 250))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.left_img = QtGui.QLabel(self.centralWidget)
        self.left_img.setGeometry(QtCore.QRect(20, 30, 320, 320))
        self.left_img.setText(_fromUtf8(""))
        self.left_img.setTextFormat(QtCore.Qt.AutoText)
        self.left_img.setObjectName(_fromUtf8("left_img"))
        self.webView_map = QtWebKit.QWebView(self.centralWidget)
        self.webView_map.setGeometry(QtCore.QRect(710, 410, 400, 250))
        self.webView_map.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView_map.setObjectName(_fromUtf8("webView_map"))
        self.lidar_label = QtGui.QLabel(self.centralWidget)
        self.lidar_label.setGeometry(QtCore.QRect(880, 350, 111, 31))
        self.lidar_label.setObjectName(_fromUtf8("lidar_label"))
        self.lidar_graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.lidar_graphicsView.setGeometry(QtCore.QRect(710, 30, 400, 320))
        self.lidar_graphicsView.setObjectName(_fromUtf8("lidar_graphicsView"))
        self.time_display = QtGui.QLabel(self.centralWidget)
        self.time_display.setGeometry(QtCore.QRect(90, 0, 191, 20))
        self.time_display.setText(_fromUtf8(""))
        self.time_display.setObjectName(_fromUtf8("time_display"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1159, 22))
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
        self.brake_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.throttle_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.angle_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.velocity_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.gear_textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.time_label.setText(_translate("MainWindow", "ROS time", None))
        self.lidar_label.setText(_translate("MainWindow", "Lidar", None))

from PyQt4 import QtWebKit
