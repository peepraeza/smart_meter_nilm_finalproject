float I1 = 1.11;
float I2 = 2.22;
float I3 = 3.33;
float I4 = 4.44;

float P1 = 55.55;
float P2 = 66.66;
float P3 = 77.77;
float P4 = 88.88;

float S1 = 999.99;
float S2 = 989.99;
float S3 = 976.99;
float S4 = 969.99;

#include <SoftwareSerial.h>

SoftwareSerial NanoSerial(3, 2); // RX | TX

void setup(){  
  Serial.begin(9600);
  NanoSerial.begin(4800);           
}

void loop(){

  Serial.print(I1); 
  Serial.print('\t');
  Serial.print(I2); 
  Serial.print('\t');
  Serial.print(I3); 
  Serial.print('\t');
  Serial.print(I4); 
  Serial.print('\t');
  Serial.print(P1); 
  Serial.print('\t');
  Serial.print(P2); 
  Serial.print('\t');
  Serial.print(P3); 
  Serial.print('\t');
  Serial.print(P4);
  Serial.print('\t');
  Serial.print(S1); 
  Serial.print('\t');
  Serial.print(S2); 
  Serial.print('\t');
  Serial.print(S3); 
  Serial.print('\t');
  Serial.print(S4);
  Serial.println();
  
  NanoSerial.print('\r');
  NanoSerial.print(I1); 
  NanoSerial.print(" ");
  NanoSerial.print(I2); 
  NanoSerial.print(" ");
  NanoSerial.print(I3); 
  NanoSerial.print(" ");
  NanoSerial.print(I4); 
  NanoSerial.print(" ");
  NanoSerial.print(P1); 
  NanoSerial.print(" ");
  NanoSerial.print(P2); 
  NanoSerial.print(" ");
  NanoSerial.print(P3); 
  NanoSerial.print(" ");
  NanoSerial.print(P4);
  NanoSerial.print(" ");
  NanoSerial.print(S1); 
  NanoSerial.print(" ");
  NanoSerial.print(S2); 
  NanoSerial.print(" ");
  NanoSerial.print(S3); 
  NanoSerial.print(" ");
  NanoSerial.print(S4);
  NanoSerial.print('\n');
  delay(500);
}
