#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
#include <ESP8266HTTPClient.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <EEPROM.h>
SoftwareSerial NodeSerial(D5,D6); // RX | TX

#define button D0
#define ConfigWiFi_Pin button
#define ESP_AP_NAME "NodeMCU Config WiFi"

#define led_wifi D1
#define led_mqtt D2
#define led_send_data D3
#define SERVER_NAME "http://rasppi-ip.herokuapp.com/show_ip.php"

const char* mqttServer = "";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "peepraeza";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "029064755";  // if you don't have MQTT Password, no need input
WiFiClient espClient;
String readString;
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button

PubSubClient client(espClient);
WiFiManager wifiManager;
void setup() {

  pinMode(ConfigWiFi_Pin, INPUT);
  pinMode(led_wifi, OUTPUT);
  pinMode(led_mqtt, OUTPUT);
  pinMode(led_send_data, OUTPUT);
  
  digitalWrite(led_wifi,LOW);
  digitalWrite(led_mqtt,LOW);
  digitalWrite(led_send_data,LOW);
  
  Serial.begin(9600);
  NodeSerial.begin(4800);
  WIFI_Connect();
  Serial.println( "Go to MQTT" );
  MQTT_Connect();
}

void WIFI_Connect(){
  WiFi.begin(EEPROM_ESP8266_LEER(0,32).c_str(), EEPROM_ESP8266_LEER(32,64).c_str());
  while(WiFi.status() != WL_CONNECTED){
    delay ( 250 );
    digitalWrite(led_wifi, HIGH);
    Serial.print ( "." );
    delay ( 250 );
    digitalWrite(led_wifi, LOW);
    buttonState = digitalRead(ConfigWiFi_Pin);
    if (buttonState != lastButtonState) {
      if (buttonState == HIGH) {
        Serial.println("-------RESET--------");
        digitalWrite(led_wifi, LOW);
        resetWifi();
      }
      delay(50);
    }
    lastButtonState = buttonState;
    yield();
    }
   Serial.println("WiFi connected");  
   digitalWrite(led_wifi, HIGH);
}

void resetWifi(){
  wifiManager.resetSettings();
  wifiManager.autoConnect(ESP_AP_NAME); 
  Serial.println(WiFi.SSID());
  Serial.println(WiFi.psk());
  if(WiFi.status() == WL_CONNECTED){
    EEPROM_ESP8266_GRABAR(WiFi.SSID(), 0); //Primero de 0 al 32, del 32 al 64, etc
    EEPROM_ESP8266_GRABAR(WiFi.psk(), 32); //SAVE
    Serial.println("Save");
  }
}
  
void MQTT_Connect(){
  if (client.connected()){Serial.println("MQTT Connected");}
  while (!client.connected()) {
    if(WiFi.status() != WL_CONNECTED){
      digitalWrite(led_mqtt, LOW);
      WIFI_Connect();
    }
     
    HTTPClient http;
    Serial.println("[HTTP] starting...\n");
    http.begin(SERVER_NAME);
    int httpCode = http.GET();
    String payload = http.getString();   
    Serial.print("[HTTP] GET...\n");
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
    int length = payload.length()+1;
    char server_ip[length];
    payload.toCharArray(server_ip, length);
    client.setServer(server_ip, mqttPort);
    client.setCallback(callback);
    client.connect("ESP8266Client", mqttUser, mqttPassword);
    Serial.println("Connecting to MQTT...");
    for (int i = 0; i < 25; i++){
        delay ( 100 );
        digitalWrite(led_mqtt, HIGH);
        Serial.print ( "." );
        delay ( 100 );
        digitalWrite(led_mqtt, LOW);
      }
      yield();
    }
  Serial.println("MQTT Connected");
  digitalWrite(led_mqtt, HIGH);
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
  digitalWrite(led_send_data, HIGH);
}

void EEPROM_ESP8266_GRABAR(String buffer, int N) {
  EEPROM.begin(512); delay(10);
  for (int L = 0; L < 32; ++L) {
    EEPROM.write(N + L, buffer[L]);
  }
  EEPROM.commit();
}

String EEPROM_ESP8266_LEER(int min, int max) {
  EEPROM.begin(512); delay(10); String buffer;
  for (int L = min; L < max; ++L){
      buffer += char(EEPROM.read(L));
  }
  return buffer;
}

void loop() {
  
  while (NodeSerial.available() > 0){
   // if Press a button for reset wifi
   buttonState = digitalRead(ConfigWiFi_Pin);
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      
      digitalWrite(led_wifi, LOW);
      Serial.println("-------RESET--------");
      wifiManager.resetSettings();
      WIFI_Connect();
    }
    delay(50);
  }
  lastButtonState = buttonState;    
  
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
    
    digitalWrite(led_send_data, LOW);
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
  } 
  
}
