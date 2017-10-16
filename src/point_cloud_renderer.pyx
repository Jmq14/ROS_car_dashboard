from libc.stdlib cimport malloc, free

cdef extern from "lidar_reading.hpp":
  cdef cppclass LidarReading:
    float x
    float y
    float z
    float intensity
    float ring
    float rotation
    float revolution

cdef extern from "point_cloud_renderer.hpp":
  cdef cppclass PointCloudRenderer:
    PointCloudRenderer(int total_readings) except +
    void init_GL()
    void render_frame()
    void load_reading(LidarReading reading)
    void load_xyzi_pc_and_render(const char *data, 
                                 int length)
    void clear_readings()
    void set_screen_size(int w, int h)
    void rotate_camera(float dx, float dy)

cdef class LIDARPointCloudRenderer:
  cdef PointCloudRenderer *pcr
  def __cinit__(self, int total_readings=262144):
    self.pcr = new PointCloudRenderer(total_readings)

  def init_GL(self):
    self.pcr.init_GL()

  def render_frame(self):
    self.pcr.render_frame()

  def load_reading(self, x, y, z, intensity, ring, 
                   rotation, revolution):
    cdef LidarReading reading
    reading.x = x
    reading.y = y
    reading.z = z
    reading.intensity = intensity
    reading.ring = ring
    reading.rotation = rotation
    reading.revolution = revolution
    self.pcr.load_reading(reading)

  def load_xyzi_pc_and_render(self, data):
    self.pcr.load_xyzi_pc_and_render(data, len(data))

  def clear_readings(self):
    self.pcr.clear_readings()

  def set_screen_size(self, w, h):
    self.pcr.set_screen_size(w, h)

  def rotate_camera(self, dx, dy):
    self.pcr.rotate_camera(dx, dy)
