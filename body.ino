#include<i2c_t3.h>

struct typeServo {int8_t pwm_pin; int8_t monitor_pin; int8_t dir; float lower_lim; float upper_lim; float angular_range; float mid_pos; float des_pos;};
const int n_servos = 6;
typeServo servo [n_servos] = { 
  { 2 , -1, 1, 0.50, 2.30, 210, 1.35, 1.35},
  { 3 , -1, 1, 0.50, 2.10, 180, 1.44, 1.44},
  { 4 , -1, 1, 2.60, 0.6 , 180, 0.9 , 0.9 },
  { 5 , -1, 1, 0.50, 2.10, 190, 1.30, 1.30},
  { 6 , -1, 1, 0.60, 2.20, 170, 1.40, 1.40},
  { 7 , -1, 1, 0.70, 2.40, 190, 1.50, 1.50},};

struct typeServo360 {int8_t pwm_pin; int8_t monitor_pin; int8_t dir; float lower_lim; float upper_lim; float dead_range; float vel_range; float mid_pos; float des_pos;};
const int n_servos360 = 2;
typeServo360 servo360 [n_servos360] = { 
  { 8 , 11, 1, 1.27, 1.73, 0.03, 2*2.0, 1.5, 1.5},
  { 9 , 12, 1, 1.27, 1.73, 0.03, 2*2.0, 1.5, 1.5},};


const int n_axons_in = 3;
const int n_axons_out = 3;
union {
   byte b[4];
   float val;
} data[n_axons_in];


unsigned long time_interrupt_0 = micros();
unsigned long time_interrupt_1 = micros();
int time_pwm_pos_0 = micros();
int time_pwm_pos_1 = micros();

uint8_t force[3];

int8_t info = 0;
const int n_commands = 4;
int commands[n_commands] = {0,0,0,0};




// ****************************************************************
// *********************   SETUP        ***************************
// ****************************************************************

void setup() {
  Serial.begin(1000000);
  for (int i; i<n_servos; i++){ 
    pinMode(servo[i].pwm_pin, OUTPUT);
  }
  
  for (int i=0; i<n_servos; i++){ 
    analogWriteFrequency(servo[i].pwm_pin, 100); //changes frequency of all the pwms hooked up to this port, see https://www.pjrc.com/teensy/td_pulse.html
  }
  analogWriteResolution(12);   
  analogReadResolution(12);
}

// ****************************************************************
// *********************   MAIN         ***************************
// ****************************************************************

void loop() {

  // ********************* COMM with BRAIN **************************
  // O--> BRAIN -->o
  // O--> BRAIN -->o
  // O--> BRAIN -->o

  uint8_t n_available = Serial.available();
  if (n_available > 0){ 
    if (n_available == n_commands){
      for (int i=0; i<n_commands; i++){
        commands[i] = Serial.read();
      }
      info += 16;
    }
    else{
      for (int i=0; i<n_available; i++){
        Serial.read();
      }
      info += 32;
    }

    for (int i=0; i<3; i++){
      Serial.write(force[i]);
      //commands[i] += 1;
      //Serial.write(commands[i]);
    }
    for (int i=0; i<n_commands; i++){
      Serial.write(commands[i]);
      //commands[i] += 1;
      //Serial.write(commands[i]);
    }
    Serial.write(info);
    info = 0;
  }

  // *********************   ACT          ***************************
  // o-->
  // o-->
  // o-->

  float scale = 1000.0;
  float x = 0.1 + (float)(commands[0]) / scale ;
  float y = (float)(commands[1]) / scale ;
  float z = (float)(commands[2]) / scale ; ;
  float robot_angle[6];
  robotIK(&x, &y, &z, robot_angle);
  
  for (int i=0; i<n_servos; i++){ 
    servo[i].des_pos = servo[i].mid_pos + robot_angle[i] / (servo[i].angular_range / (servo[i].upper_lim - servo[i].lower_lim));
    analogWrite(servo[i].pwm_pin, int(servo[i].des_pos / 10.0 * 4096.0));
  }

  // *********************   SENSE        ***************************
  // -->O
  // -->O
  // -->O
  force[0] = (uint8_t)(analogRead(A0)/16);
  force[1] = (uint8_t)(analogRead(A1)/16);
  force[2] = (uint8_t)(analogRead(A2)/16);
  
  delay(100);
  
}
