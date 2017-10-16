#ifndef CAMERA_H__
#define CAMERA_H__

#include <math.h>
#include <iostream>

#include "glm/glm.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtc/type_ptr.hpp"

#define GLM_ENABLE_EXPERIMENTAL
#include "glm/gtx/rotate_vector.hpp"

const double PI = std::acos(-1);

class Camera {

  glm::vec3 position;
  glm::vec3 target;
  glm::vec3 up;

  public:

  double x;
  double y;

  Camera(glm::vec3 pos, glm::vec3 t, glm::vec3 u): 
         position(pos), up(u), target(t) {
    position = pos;
    target = t;
    up = u;
    modelview = glm::lookAt(position, target, up); 
  }

  void set_position(float x, float y, float z);
  void set_target(float x, float y, float z);
  void set_up(float x, float y, float z);
  void set_screen_size(int w, int h);
  void update_screensize(int w, int h);
  void update_modelview();
  
  void rotate(float dx, float dy);

  glm::mat4 modelview;
  glm::mat4 projection;
};

#endif
