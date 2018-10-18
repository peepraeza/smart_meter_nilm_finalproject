float I1 = 1.11;
float I2 = 2.22;
float I3 = 3.33;
float I4 = 4.44;

float P1 = 10.11;
float P2 = 20.22;
float P3 = 30.33;
float P4 = 40.44;

float S1 = 100.11;
float S2 = 200.22;
float S3 = 300.33;
float S4 = 400.44;

#include <SoftwareSerial.h>

SoftwareSerial NanoSerial(3, 2); // RX | TX

void setup(){  
  Serial.begin(9600);
  NanoSerial.begin(4800);           
}

void loop(){
  NanoSerial.print(I1); 
  NanoSerial.print('\t');
  NanoSerial.print(I2); 
  NanoSerial.print('\t');
  NanoSerial.print(I3); 
  NanoSerial.print('\t');
  NanoSerial.print(I4); 
  NanoSerial.print('\t');
  NanoSerial.print(P1); 
  NanoSerial.print('\t');
  NanoSerial.print(P2); 
  NanoSerial.print('\t');
  NanoSerial.print(P3); 
  NanoSerial.print('\t');
  NanoSerial.print(P4);
  NanoSerial.print('\t');
  NanoSerial.print(S1); 
  NanoSerial.print('\t');
  NanoSerial.print(S2); 
  NanoSerial.print('\t');
  NanoSerial.print(S3); 
  NanoSerial.print('\t');
  NanoSerial.print(S4);
  NanoSerial.print('\n');
  delay(500);
}
