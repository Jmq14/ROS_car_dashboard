#include "point_cloud_renderer.hpp"

void PointCloudRenderer::init_GL(glm::vec3 position, 
																 glm::vec3 target,
																 glm::vec3 up) {
	int temp = gladLoadGL();

  // VAO
  glGenVertexArrays(1, &VAO);
  glBindVertexArray(VAO);

  // VBO
  glGenBuffers(1, &VBO);
  glBindBuffer(GL_ARRAY_BUFFER, VBO);

  // Load Shader
  shader_program = LoadShader("../shaders/point_sprite_positioning.vert",
                              "../shaders/point_sprite_circle.frag");
  pos_location = glGetAttribLocation(shader_program, "pos");
  modelview_location = glGetUniformLocation(shader_program, "modelview");
  projection_location = glGetUniformLocation(shader_program, "projection");
  screenSize_location = glGetUniformLocation(shader_program, "screenSize");
  radius_location = glGetUniformLocation(shader_program, "radius");

  // Set data attributes
  glVertexAttribPointer(pos_location, 3, GL_FLOAT, false, sizeof(LidarReading), 0);

  // Initialize camera;
  camera = new Camera(position, target, up);

  glUseProgram(shader_program);
  glUniformMatrix4fv(modelview_location, 1, GL_FALSE, glm::value_ptr(camera->modelview));
  glUniformMatrix4fv(projection_location, 1, GL_FALSE, glm::value_ptr(camera->projection));
  glUniform1fv(radius_location, 1, &RADIUS);
 
  // Enable point sprites
  glEnable(GL_PROGRAM_POINT_SIZE);

}

void PointCloudRenderer::render_frame(LidarReading *readings, 
                                      const int& num_readings, 
                                      const GLuint& frame_buffer) {
  if (frame_buffer) {
    glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer);
  }

  // Reset
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glEnable(GL_DEPTH_TEST);
  
  // Bind VAO and VBO
  glBindVertexArray(VAO);
  glBindBuffer(GL_ARRAY_BUFFER, VBO);

  // Setup Shader
  glUseProgram(shader_program);
  glUniformMatrix4fv(modelview_location, 1, GL_FALSE, glm::value_ptr(camera->modelview));
  glUniformMatrix4fv(projection_location, 1, GL_FALSE, glm::value_ptr(camera->projection));

  // Try orphaning
  glBufferData(GL_ARRAY_BUFFER, sizeof(LidarReading) * num_readings, NULL, GL_STREAM_DRAW);

  // Buffer Data, need to make faster
  glBufferData(GL_ARRAY_BUFFER, sizeof(LidarReading) * num_readings, readings, GL_STREAM_DRAW);

  glVertexAttribPointer(pos_location, 3, GL_FLOAT, false, sizeof(LidarReading), 0);
  glEnableVertexAttribArray(pos_location);
  
  // Draw, maybe replace with DrawElements
  glDrawArrays(GL_POINTS, 0, num_readings);

  if (frame_buffer) {
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
  }
}

// Render the current readings that are loaded
void PointCloudRenderer::render_frame() {
  render_frame(readings, num_readings_loaded);
}

// Load a single reading into the buffer
void PointCloudRenderer::load_reading(const LidarReading& reading) {
  if (num_readings_loaded == readings_per_frame) {
    readings_per_frame *= 2;
    LidarReading* new_buffer = 
        (LidarReading *) realloc(readings, readings_per_frame * sizeof(LidarReading));
    if (!new_buffer) {
      printf("Could not add reading. No space");
      return;
    }
    readings = new_buffer;
  }
  readings[num_readings_loaded] = reading;
  num_readings_loaded++;
}

// Load a string of XYZI readings (8 bytes each) and render.
void PointCloudRenderer::load_xyzi_pc_and_render(const char *data, int len) {
  clear_readings();
  for (int j = 0; j < len; j+=32) {
    float x;
    float y;
    float z;
    
    memcpy(&x, data + j    , 4);
    memcpy(&y, data + j + 4, 4);
    memcpy(&z, data + j + 8, 4);

    LidarReading reading;
    reading.x = (float) x;
    reading.y = (float) y;
    reading.z = (float) z;
    load_reading(reading);
  }
  render_frame();
}

// Reset readings buffer to load from beginning
void PointCloudRenderer::clear_readings() {
  num_readings_loaded = 0;
}

// Set screen size in pixels.
void PointCloudRenderer::set_screen_size(const int& w, const int& h) {
  screensize.x = w;
  screensize.y = h;
  
  camera->set_screen_size(w, h);

  glUniform2fv(screenSize_location, 1, glm::value_ptr(screensize));
}

// Rotate the camera according to mouse input. Currently only rotates about the z-axis
void PointCloudRenderer::rotate_camera(float dx, float dy) {
  camera->rotate(dx, dy);
  glUniformMatrix4fv(modelview_location, 1, GL_FALSE, glm::value_ptr(camera->modelview));
}
