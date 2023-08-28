attribute vec3 kzPosition;
attribute vec2 kzTextureCoordinate0;

uniform highp mat4 kzProjectionCameraWorldMatrix;
uniform mediump vec2 TextureOffset;
uniform mediump vec2 TextureTiling;

uniform lowp float x0;
uniform lowp float y0;
uniform lowp float x1;
uniform lowp float y1;
uniform lowp float x2;
uniform lowp float y2;
uniform lowp float x3;
uniform lowp float y3;
uniform lowp float x4;
uniform lowp float y4;
uniform lowp float mesh_x_len;
uniform lowp float mesh_y_len;
uniform lowp float mesh_arrow_ratio;

varying mediump vec2 vTexCoord;


// CONFIGURABLE VARIABLES.
const bool SMOOTH_SHIFT = true;

const int c_len = 9; // Length of con.
const int fp_len = 4; // Length of fake.
const int vc_len = c_len+fp_len;

const float threshold = 0.5; // Bezier curve midpoint threshold.
const float y_capacity = 50.0; // Adjustment for y point input.
const float arrow_point_to_stem_ratio = 0.5; // Meaning that length(arrow's point) / length(arrow's stem) = 0.3/1.


// Program variables.
vec2 con[c_len];
vec2 fake[fp_len];
vec2 v_con[vc_len];
vec2 qt[2]; // This denote q points based on t.


// Level 3: Helper functions.
vec2 _offset(vec2 point, float d_x, float d_y) {
  // Adds dy and dx to the point.
  return vec2(point.x + d_x, point.y + d_y);
} 

int _modulo(int n, int p) {
  // Calculates n % p.
  while (n >= p) n = n-p;
  return n;
}


// Level 2: Computing aid functions.
void init_con(float x_offset, float y_offset) { // NOTE: Relies on hardcoding.
  // Sets up the original con points at 0, 2, 4, 6, 8.
  con[0] = _offset(vec2(x0, y0), x_offset, y_offset);
  con[2] = _offset(vec2(x1, y1), x_offset, y_offset);
  con[4] = _offset(vec2(x2, y2), x_offset, y_offset);
  con[6] = _offset(vec2(x3, y3), x_offset, y_offset);
  con[8] = _offset(vec2(x4, y4), x_offset, y_offset);
  
  // Sets up the middle con points (depending on the threshold) at 1, 3, 5, 7.
  con[1] = mix(con[0], con[2], threshold);
  con[3] = mix(con[2], con[4], threshold);
  con[5] = mix(con[4], con[6], threshold);
  con[7] = mix(con[6], con[8], threshold);
}

float calc_vert_dist() {
  // Calculates the cumulative vertical distance of the con points.
  float vert_dist = 0.;
  vert_dist = (con[c_len-1] - con[0]).x * (1.0+arrow_point_to_stem_ratio);
  return vert_dist;
}

void init_fake(float vert_dist) { // NOTE: Relies on hardcoding.
  // Sets up the original fake points at 1, 3.
  fake[1] = vec2(con[c_len-1].x+(vert_dist-con[c_len-1]).x/2.0, con[c_len-1].y);
  fake[3] = vec2(vert_dist, con[c_len-1].y);
  
  // Sets up the middle fake points (depending on the threshold) at 0, 2.
  fake[0] = mix(con[c_len-1], fake[1], threshold);
  fake[2] = mix(fake[1], fake[3], threshold);
}

void scale_v_con(float scale) {
  // Scales the v_con points.
  for (int i=0; i<c_len; ++i) v_con[i] = con[i]*scale;
  for (int i=0; i<fp_len; ++i) v_con[i+c_len] = fake[i]*scale;
}

int bezier_inds(int k) {
  // Finds the indices useful for bezier curve generation.
  if (k==0) return k; 
  else if (k==vc_len-2) return k-1; 
  else if (_modulo(k, 2)==0) return k-1;
  else return k;
}

vec2 bezier_func(int c_ind, float t) {
  // Calculates b(t).
  // Setting up the q1 and q2 points.
  vec2 p0 = v_con[c_ind], p1 = v_con[c_ind+1], p2 = v_con[c_ind+2];
  vec2 q0 = mix(p0, p1, t); vec2 q1 = mix(p1, p2, t);
  qt[0] = q0; qt[1] = q1;

  // Getting the shift distance. 
  vec2 shift_distance = mix(q0, q1, t);
  return shift_distance;
}

void get_perp(vec2 v, out vec2 vp1, out vec2 vp2) {
  // Set the last two positional arguments as the perpendicular unit vectors of v.
  vec2 v_unit = normalize(v);
  vp1 = vec2(v_unit.y, -v_unit.x);
  vp2 = vec2(-v_unit.y, v_unit.x);
}

vec2 calc_tangent() {
  // Calculates the tangent vector at b(t)
  return qt[1]-qt[0];
}

void directional_shift(out vec3 pos, out vec2 u_perp, float dist_from_mid) {
  // Adds the vec2 onto the vec3.
  vec2 perp = u_perp * abs(dist_from_mid);
  pos.y = pos.y + perp.y; pos.x = pos.x + perp.x;
}


// Level 1: Core functions.
void init_v_con() {
  // Sets up the v_con points.
  // Initializing con points.
  float x_offset = -x0; float y_offset = -y_capacity/2.0;
  init_con(x_offset, y_offset);

  // Adding up the entire spine distance.
  float vert_dist = calc_vert_dist();

  // Adding fake points to indicate arrow position.
  init_fake(vert_dist);
    
  // Scaling the points.
  float scale = mesh_x_len / vert_dist;
  scale_v_con(scale);
}

bool in_range(float x, float r1, float r2) {
  // Compares if x is in range of r1 and r2.
  return (x >= r1) && (x <= r2);
}

vec2 calc_shift(int i, vec3 pos) {
  // Calculates the shifting vector.
  int c_ind = bezier_inds(i);
  float t = smoothstep(v_con[c_ind].x, v_con[c_ind+2].x, pos.x);
  return bezier_func(c_ind, t);
}

void apply_shift(out vec3 pos, vec2 shift) {
  // Applies the shifting vector onto pos.
  vec2 u_perp1, u_perp2; get_perp(calc_tangent(), u_perp1, u_perp2);
  
  float dist_from_mid = pos.y;
  pos.y = shift.y; pos.x = shift.x;
  
  if (SMOOTH_SHIFT) {
    if (u_perp1.y * dist_from_mid >= 0.0)
      directional_shift(pos, u_perp1, dist_from_mid);
    else
      directional_shift(pos, u_perp2, dist_from_mid);
  }
  else pos.y = pos.y + dist_from_mid;
}

void post_process(vec3 pos) {
  // Handles camera post-processing.
  vTexCoord = kzTextureCoordinate0*TextureTiling + TextureOffset;
  gl_Position = kzProjectionCameraWorldMatrix * vec4(pos, 1.0);
}


// Level 0: Main function.
void main() {
  // Executes the point-shifting algorithm.
  // Setting up.
  precision lowp float;
  vec3 pos = kzPosition;
  
  // Initializing the v_con (visual con) array.
  init_v_con();
  
  // Shifting at the correct interval.
  for (int i=0; i<vc_len-1; ++i) {
    if (in_range(pos.x, v_con[i].x, v_con[i+1].x)) { // Finding the correct interval.
      vec2 shift = calc_shift(i, pos); // Calculating how much to shift.
      apply_shift(pos, shift); // Shifting it.
      break;
    }
  }

  // Post processing.
  post_process(pos);
}

