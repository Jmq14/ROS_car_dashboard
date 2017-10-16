#ifndef LIDAR_READING_H__
#define LIDAR_READING_H__

struct LidarReading {
  float x;
  float y;
  float z;
  float intensity;
  float ring;
  float rotation;
  float revolution;
};


#endif
