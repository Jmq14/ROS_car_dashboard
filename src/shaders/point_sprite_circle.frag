#version 330

// Parameters from the vertex shader
in vec3 eyespacePos;
in float eyespaceRadius;
in float dist_from_origin;

// Uniforms
uniform mat4 modelview;
uniform mat4 projection;
uniform vec2 screenSize;

// Heat map values
uniform vec4 red = vec4(1.0f, 0, 0, 1.0f);
uniform vec4 yellow = vec4(1.0f, 1.0f, 0, 1.0f);
uniform vec4 green = vec4(0.5f, 1.0f, 0.0f, 1.0f);
uniform vec4 blue = vec4(0.0f, 0.5f, 1.0f, 1.0f);

// Output
out vec4 vFragColor;

vec4 heat_map_color(float dist) {
  // dist should be normalized between 0 and 1
  float close  = float(dist < 0.34f);
  float medium = float(dist >= 0.34f && dist < 0.67f);
  float far    = float(dist >= 0.67f);
    
  vec4 close_value = ((0.34f - dist) * red + dist * yellow) / .34f;
  vec4 medium_value = ((0.34f - dist / 2.0f) * yellow + dist / 2.0f * green) / .34f;
  vec4 far_value = ((0.34f - (min(dist, 1.0f) / 3.0f)) * green + min(dist, 1.0f) / 3.0 * blue) / .34f;

  return close * close_value + medium * medium_value + far * far_value;

  //if (dist < 0.34f) {
  //  return ;
  //}
  //else if (dist < 0.67f) {
  //  dist /= 2.0f;
  //}
  //else {
  //  dist = min(1.0f, dist);
  //  dist /= 3.0f;
  //  return ;
  //}
}

void main() {
  vec3 normal;

  // See where we are inside the point sprite
  normal.xy = (gl_PointCoord * 2.0f) - vec2(1.0);
  float dist = dot(normal.xy, normal.xy);
  
  // Discard if outside circle 
  //if(dist > 1.0f) {
  //  discard;
  //}

  vFragColor = heat_map_color (dist_from_origin / 40.0f) ;

  // Calculate fragment position in eye space, project to find depth
  vec4 fragPos = vec4(eyespacePos + normal * eyespaceRadius, 1.0);
  vec4 clipspacePos = projection * fragPos;

  // Set up output
  float far = gl_DepthRange.far; 
  float near = gl_DepthRange.near;
  float deviceDepth = clipspacePos.z / clipspacePos.w;
  float fragDepth = (((far - near) * deviceDepth) + near +far) / 2.0;
  gl_FragDepth = fragDepth;
}
