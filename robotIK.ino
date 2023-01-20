// Inverse Kinematic for robot arm with 6DOF

void robotIK(float* x, float* y, float* z, float* robot_angle){
  //Converts x y z coordinates in [m] to robot angles [deg]
  float r_offset = 0.03;
  float a = 0.118;
  float c = 0.130;
  
  float r = sqrt(*x * *x + *y * *y) - r_offset;
  float delta = atan2(*z, r);
  float b = sqrt(r*r + *z * *z);
  
  float rho = atan2(*y, *x);  
  float gamma = acos( (a*a + b*b -c*c) / (2 * a * b));
  float beta = acos( (a*a + c*c -b*b) / (2 * a * c));
  
  robot_angle[0] = 180 / PI * rho;
  robot_angle[1] = 180 / PI * (gamma + delta) - 90; // note that 90 is with respect to servo 0 conventiona
  robot_angle[2] = 180 / PI * beta + robot_angle[1] - 90;
  robot_angle[3] = 0;
  robot_angle[4] = -90 - robot_angle[2];
  robot_angle[5] = robot_angle[0];
}
