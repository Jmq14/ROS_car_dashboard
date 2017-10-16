import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor, QApplication, QMessageBox, QSlider, QWidget
from PyQt4.QtOpenGL import QGL, QGLFormat, QGLWidget

from point_cloud_renderer import *

try:
  from OpenGL import GL
except ImportError:
  app = QApplication(sys.argv)
  QMessageBox.critical(None, "LIDAR Visualization",
          "PyOpenGL must be installed to run this example.")
  sys.exit(1)


class LIDARVisualizer(QGLWidget):
  GL_MULTISAMPLE = 0x809D
  rot = 0.0

  def __init__(self, parent, bag=None):
    self.bag = bag
      
    f = QGLFormat.defaultFormat()
    f.setVersion(3, 2)
    f.setProfile(QGLFormat.CoreProfile)
    super(LIDARVisualizer, self).__init__(f, parent)

    self.lidar =  LIDARPointCloudRenderer()

    self.setMouseTracking(True)
    
    self.last_x = 0
    self.last_y = 0


    if self.bag:
      import rosbag
      print("Loading LIDAR data")
      self.readings = [msg.message.data for msg in rosbag.Bag(self.bag)
                       if msg.topic == '/velodyne_points']
      
      self.scrubber = QSlider(Qt.Horizontal, self)
      self.scrubber.valueChanged.connect(self.set_frame)
      
      self.scrubber.setTickInterval(1)
      self.scrubber.setMinimum(0)
      self.scrubber.setMaximum(len(self.readings) - 1)

      self.setWindowTitle("LIDAR Visualization")

  def set_frame(self):
    self.load_xyzi_pc_and_render(self.readings[self.scrubber.value()])    

  def initializeGL(self):
    self.lidar.init_GL()

  def resizeGL(self, w, h):
    GL.glViewport(0, 0, w, h)
    self.lidar.set_screen_size(w, h)

  def paintGL(self):
    self.lidar.render_frame() 
  
  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.last_x = event.x()
      self.last_y = event.y()

  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.LeftButton:
      new_x = event.x()
      new_y = event.y()
      self.lidar.rotate_camera(new_x - self.last_x,
                               new_y - self.last_y)
      self.last_x = new_x
      self.last_y = new_y
      self.update()
      
  def load_xyzi_pc_and_render(self, data):
    self.lidar.load_xyzi_pc_and_render(data)

  # Load a single LIDAR reading
  # One point in the point cloud
  def load_reading(self, reading):
    self.lidar.load_reading(*reading)

  def clear_readings(self):
    self.lidar.clear_readings()
  
  # Load a LIDAR point cloud CSV file
  def load_file(self, filename):
    with open(filename) as f:
      for line in f:
        reading = line.split(",")
        reading = [float(x) for x in reading]
        self.lidar.load_reading(*reading)

if __name__ == '__main__':
  import rosbag

  app = QApplication(sys.argv[:1])
  if len(sys.argv) == 1:
    print("Please pass in a ROS bag.")

  f = QGLFormat.defaultFormat()
  f.setVersion(3, 2)
  f.setProfile(QGLFormat.CoreProfile)
  QGLFormat.setDefaultFormat(f)

  if not QGLFormat.hasOpenGL():
      QMessageBox.information(None, "LIDAR Visualization",
              "This system does not support OpenGL.")
      sys.exit(0)
  
  widget = LIDARVisualizer(None, sys.argv[1])
  
  widget.resize(1280, 720)

  widget.show()

  sys.exit(app.exec_())

