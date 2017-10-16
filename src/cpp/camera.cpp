#include "camera.hpp"

inline float clip(const float& n, const float& lower, const float& upper)
{   
  return glm::max(lower, glm::min(n, upper));
}

// Rotate camera position as a function of a 2d translation
void Camera::rotate(float dx, float dy) {
  float phi = dx*0.01;

  if (abs(dy) > 0) {
    glm::mat4 rotx = glm::rotate(phi, glm::vec3(0.0f, 0.0f, 1.0f));
    modelview = modelview * rotx;
  }
}

void Camera::set_position(float x, float y, float z) {
  position.x = x;
  position.y = y;
  position.z = z;
}

void Camera::set_target(float x, float y, float z) {
  target.x = x;
  target.y = y;
  target.z = z;
}

void Camera::set_up(float x, float y, float z) {
  up.x = x;
  up.y = y;
  up.z = z;
}

void Camera::set_screen_size(int width, int height) {
  projection = glm::perspective(45.0f, (float)width/(float)height, 0.1f, 100.0f);
}

void Camera::update_screensize(int w, int h) {
  projection = glm::perspective(45.0f, (float)w/(float)h, 0.1f, 100.0f);  
}

void Camera::update_modelview() {
  modelview = glm::lookAt(position, target, up);
}


