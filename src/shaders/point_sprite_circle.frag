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

  if (dist < 0.34f) {
    return ((0.34f - dist) * red + dist * yellow) / .34f;
  }
  else if (dist < 0.67f) {
    dist /= 2.0f;
    return ((0.34f - dist) * yellow + dist * green) / .34f;
  }
  else {
    dist = min(1.0f, dist);
    dist /= 3.0f;
    return ((0.34f - dist) * green + dist * blue) / .34f;
  }
}

void main() {
  vec3 normal;

  // See where we are inside the point sprite
  normal.xy = (gl_PointCoord * 2.0f) - vec2(1.0);
  float dist = dot(normal.xy, normal.xy);
  
  // Discard if outside circle 
  if(dist > 1.0f) {
    discard;
  }

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
