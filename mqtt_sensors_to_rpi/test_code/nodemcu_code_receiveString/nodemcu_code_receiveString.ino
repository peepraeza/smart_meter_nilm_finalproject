#include <ESP8266WiFi.h>

#include <SoftwareSerial.h>

SoftwareSerial NodeSerial(D2,D3); // RX | TX
String readString;
void setup() {

  pinMode(D2, INPUT); 

  pinMode(D3, OUTPUT); 

  Serial.begin(9600);

  NodeSerial.begin(4800);

  Serial.println();

  Serial.println();

  Serial.println("NodeMCU/ESP8266 Run");

 }

void loop() {

  while (NodeSerial.available()) {
    char c = NodeSerial.read();  //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2);  //slow looping to allow buffer to fill with next character
  }

  if (readString.length() >0) {
    Serial.println(readString);  //so you can see the captured String 
    readString="";
  } 


//  delay(500);

} 
