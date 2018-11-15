#include "EmonLib.h"             // Include Emon Library
#include <SoftwareSerial.h>
EnergyMonitor emon1, emon2, emon3, emon4;             // Create an instance
SoftwareSerial NanoSerial(9, 8); // RX | TX   

String data;                                                                            
void setup(){  
  Serial.begin(9600);
  NanoSerial.begin(4800);    
  pinMode(LED_BUILTIN, OUTPUT);   
  emon1.current(1, 58.6);       // Current: input pin, calibration.
  emon1.voltage(0, 285.5, 1.7);  // Voltage: input pin, calibration, phase_shift
  
  emon2.current(2, 58.6);       // Current: input pin, calibration.
  emon2.voltage(0, 285.5, 1.7);
  
  emon3.current(3, 58.6);       // Current: input pin, calibration.
  emon3.voltage(0, 285.5, 1.7);

  emon4.current(4, 58.6);       // Current: input pin, calibration.
  emon4.voltage(0, 285.5, 1.7);    
}

void loop() {

  emon1.calcVI(20,2000);         // Calculate all. No.of half wavelengths (crossings), time-out
  emon2.calcVI(20,2000);
  emon3.calcVI(20,2000);
  emon4.calcVI(20,2000);
  
  float realPower1       = emon1.realPower;        //extract Real Power into variable
  float realPower2       = emon2.realPower;        
  float realPower3       = emon3.realPower;        
  float realPower4       = emon4.realPower;
  
  float apparentPower1   = emon1.apparentPower;    //extract Apparent Power into variable
  float apparentPower2   = emon2.apparentPower;
  float apparentPower3   = emon3.apparentPower;
  float apparentPower4   = emon4.apparentPower;
  
  float Irms1            = emon1.Irms;             //extract Irms into Variable
  float Irms2            = emon2.Irms;             
  float Irms3            = emon3.Irms;             
  float Irms4            = emon4.Irms;

  data = "START,"+String(Irms1)+","+String(Irms2)+","+String(Irms3)+","+String(Irms4);
  data += ","+String(abs(realPower1))+","+String(abs(realPower2))+","+String(abs(realPower3))+","+String(abs(realPower4));
  data += ","+String(abs(apparentPower1))+","+String(abs(apparentPower2))+","+String(abs(apparentPower3))+","+String(abs(apparentPower4));
  data += ",END";
                            
  Serial.print(data); 
  Serial.println();
  
  int length = data.length()+1;
  char send_data[length];
  data.toCharArray(send_data, length);
  
  NanoSerial.print(send_data); 
  digitalWrite(LED_BUILTIN, HIGH); // LED ON When data sent
  delay(500);
  digitalWrite(LED_BUILTIN, LOW); // LED OFF When data no sent

}
