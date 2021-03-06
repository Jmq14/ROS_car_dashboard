#!/usr/bin/env python

import os
import thread
import sys
from PyQt4 import QtCore, QtGui

from sensor_msgs.msg import *
from dbw_mkz_msgs.msg import *

from gui_monitor import Ui_MainWindow
from reader import Reader

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    reader = Reader()
    ui.setupReader(reader)

    thread.start_new_thread(reader.setup_subscriber, ())

    sys.exit(app.exec_())

