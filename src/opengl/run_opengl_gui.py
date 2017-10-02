#!/usr/bin/env python

import os
import thread
import sys
from PyQt4 import QtCore, QtGui

from glgui_monitor import Ui_MainWindow
from glreader import Reader

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

