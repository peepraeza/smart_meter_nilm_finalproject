float I1 = 400.56;

float I2 = 567.89;

#include <SoftwareSerial.h>

SoftwareSerial NanoSerial(3, 2); // RX | TX

void setup()

{  

  Serial.begin(9600);

  NanoSerial.begin(4800);           

}

void loop() {

  Serial.print(I1); 
  Serial.print("\t");
  Serial.println(I2);
//  NanoSerial.print(110);
//  NanoSerial.print("\t");
  NanoSerial.print(I1);
  NanoSerial.print('\t');
  NanoSerial.print(I2); 
//  NanoSerial.print(1234567890);
  NanoSerial.print('\n');

  delay(500);

}
