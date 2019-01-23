#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
SoftwareSerial NodeSerial(D2,D3); // RX | TX

const char* ssid = "Peerawit-WiFi";                   // wifi ssid
const char* password =  "p12345678";         // wifi password
const char* mqttServer = "192.168.0.102";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "peepraeza";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "029064755";  // if you don't have MQTT Password, no need input
WiFiClient espClient;
String readString;
PubSubClient client(espClient);

void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(9600);
  NodeSerial.begin(4800);
  WIFI_Connect();
  MQTT_Connect();
}

void WIFI_Connect(){
  digitalWrite(2,1);
  Serial.println("Booting Sketch...");
  while(WiFi.status() != WL_CONNECTED){
    WiFi.disconnect();
    WiFi.begin("Peerawit-WiFi", "p12345678");
    for (int i = 0; i < 25; i++){
        delay ( 250 );
        digitalWrite(2,0);
        Serial.print ( "." );
        delay ( 250 );
        digitalWrite(2,1);
      }
      yield();
    }
  digitalWrite(2,0);
}

void MQTT_Connect(){
  digitalWrite(2,1); // LED OFF
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  client.connect("ESP8266Client", mqttUser, mqttPassword);
  if (client.connected()){Serial.println("MQTT Connected");}
  while (!client.connected()) {
    if(WiFi.status() != WL_CONNECTED){
      WIFI_Connect();
     }
    client.connect("ESP8266Client", mqttUser, mqttPassword);
    Serial.println("Connecting to MQTT...");
    for (int i = 0; i < 25; i++){
        delay ( 100 );
        digitalWrite(2,0);
        Serial.print ( "." );
        delay ( 100 );
        digitalWrite(2,1);
      }
      yield();
    }
  digitalWrite(2,0);
 }

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------");
  digitalWrite(2,0);
}


void loop() {
  while (NodeSerial.available() > 0){
      // if wi-fi disconnected 
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("No WiFi connected");
      WIFI_Connect();
    }
    
    // if MQTT server disconnected
    if (!client.connected()) {
      Serial.println("No MQTT connected");
      MQTT_Connect();
    }
    
    digitalWrite(2,1);
    while (NodeSerial.available()) {
      char c = NodeSerial.read();  //gets one byte from serial buffer
      readString += c; //makes the String readString
      delay(2);  //slow looping to allow buffer to fill with next character
    }

    if (readString.length() >0){  
      int length = readString.length()+1;
      char send_data[length];
      readString.toCharArray(send_data, length);
      
      client.publish("esp8266", send_data);
      client.subscribe("esp8266");
      readString="";
      
      client.loop();
    }
    delay(2000);
    yield();
  } 
  
}
