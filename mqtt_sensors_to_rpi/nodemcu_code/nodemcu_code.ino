#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
SoftwareSerial NodeSerial(D2,D3); // RX | TX

const char* ssid = "Peerawit-WiFi";                   // wifi ssid
const char* password =  "p12345678";         // wifi password
const char* mqttServer = "192.168.0.106";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "username";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "029064755";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(9600);
  NodeSerial.begin(4800);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("connected");
    }else{
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  
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

}


void loop() {
  while (NodeSerial.available() > 0){
    if(NodeSerial.read() == '\n'){
      float I1 = NodeSerial.parseFloat(); 
      float I2 = NodeSerial.parseFloat(); 
      float I3 = NodeSerial.parseFloat(); 
      float I4 = NodeSerial.parseFloat(); 
      
      float P1 = NodeSerial.parseFloat(); 
      float P2 = NodeSerial.parseFloat(); 
      float P3 = NodeSerial.parseFloat(); 
      float P4 = NodeSerial.parseFloat(); 
      
      float S1 = NodeSerial.parseFloat(); 
      float S2 = NodeSerial.parseFloat(); 
      float S3 = NodeSerial.parseFloat();
      float S4 = NodeSerial.parseFloat();
  
      String data = "Hello : "+String(I1)+":"+String(I2)+String(I3)+":"+String(I4)
                            +String(P1)+":"+String(P2)+String(P3)+":"+String(P4)
                            +String(S1)+":"+String(S2)+String(S3)+":"+String(S4);
                            
      int length = data.length()+1;
      char send_data[length];
      data.toCharArray(send_data, length);
      
      client.publish("esp8266", send_data);
      client.subscribe("esp8266");
      delay(500);
        
      client.loop();
    }
  }
} 
