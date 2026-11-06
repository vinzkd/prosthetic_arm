#include <Servo.h>

Servo indexServo;  

const int INDEX_PIN = 2;

void setup() {
  Serial.begin(9600);
  Serial.println("Starting serial monitor\n");
  indexServo.attach(INDEX_PIN);
  indexServo.write(90);
}

void loop() {
  // Listen to serial for Twist msg
  while (Serial.available()) {
    char c = Serial.read();
    command += c;
    if (c == '\n') { // End of command
      processTwist(command);
      command = ""; // Reset command string
    }   
  }
  indexServo.write(90);
}


void processTwist(String cmd) {
  // Example command: "1.0:0.80"
  // {linear}:{angular}
  
  cmd.trim();  // Remove whitespace
  float scale = 1.0;
  
  int colon1 = cmd.indexOf(':');
  // int colon2 = cmd.indexOf(':', colon1 + 1);

  float linearX = cmd.substring(0, colon1).toFloat();
  float angularZ = cmd.substring(colon1 + 1).toFloat();
  
 
  
  if (directive == "joystick_turn_head") { 
    int position = indexServo.read();
    position = position + (scale * angularZ);
    indexServo.write(position);
  }

}
