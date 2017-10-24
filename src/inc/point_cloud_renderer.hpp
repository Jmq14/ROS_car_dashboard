#ifndef POINT_CLOUD_RENDERER_H__
#define POINT_CLOUD_RENDERER_H__

#include "camera.hpp"
#include "glad/glad.h"
#include "GLShader.hpp"
#include "lidar_reading.hpp"

class PointCloudRenderer {
  GLuint VAO;
  GLuint VBO;

  // Locations for shader variables
  GLuint pos_location;
  GLuint modelview_location;
  GLuint projection_location;
  GLuint screenSize_location;
  GLuint radius_location;

  // Shaders
  GLuint shader_program;
  
  glm::vec2 screensize; 

  const float RADIUS = 0.03;

  int readings_per_frame;
  LidarReading* readings;
  int num_readings_loaded = 0;

  public:
  
  /* 
   * readings_per_frame is the initial size of the buffer
   */

  PointCloudRenderer(int readings_per_frame=262144) {
    this->readings_per_frame = readings_per_frame;
    readings = (LidarReading *) malloc(readings_per_frame * sizeof(LidarReading));
  }

  void init_GL(glm::vec3 position = glm::vec3(0.0, -15.0, 7.0),
               glm::vec3 target = glm::vec3(0,0,0),
               glm::vec3 up = glm::vec3(0, 0, 1));

  void render_frame(LidarReading *readings, const int& num_readings, 
                    const GLuint& frame_buffer = (GLuint) NULL);
  void render_frame();

  void load_reading(const LidarReading& reading);
  void load_xyzi_pc_and_render(const char* data, int len);
  void clear_readings();

  void set_screen_size(const int& w, const int& h);

  Camera *camera;
  void rotate_camera(float x, float y);
};

#endif
