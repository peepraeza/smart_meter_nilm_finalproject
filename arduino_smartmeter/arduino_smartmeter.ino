#include <SoftwareSerial.h>
#include "EmonLib.h"             // Include Emon Library
SoftwareSerial espSerial(10,11); /* RX:D3, TX:D2 */

#define dbgSerial   Serial   // Serial interface (USB CDC) for Debugging

#define DBG_BAUD    (19200) // baudrate for connecting the arduino uno
#define ESP_BAUD    (19200) // baudrate for connecting the ESP8266 module

#define AP_SSID          "Peerawit-WiFi"
#define AP_PASS          "p12345678"

#define SERVER_IP_ADDR    "192.168.0.104";
EnergyMonitor emon1, emon2, emon3, emon4;             // Create an instance

int reading;

const uint32_t update_interval = 8000; // msec

enum status_t { 
  ST_NONE=-1, ST_OK=0, ST_ERROR, ST_BUSY, ST_CLOSED 
};

#define BUF_SIZE      (256)

char buf[ BUF_SIZE ];
int buf_pos = 0;
String line;

void setup() {
  emon1.current(1, 58.6);       // Current: input pin, calibration.
  emon1.voltage(0, 285.5, 1.7);  // Voltage: input pin, calibration, phase_shift
  
  emon2.current(2, 58.6);       // Current: input pin, calibration.
  emon2.voltage(0, 285.5, 1.7);
  
  emon3.current(3, 58.6);       // Current: input pin, calibration.
  emon3.voltage(0, 285.5, 1.7);

  emon4.current(4, 58.6);       // Current: input pin, calibration.
  emon4.voltage(0, 285.5, 1.7);
  dbgSerial.begin( DBG_BAUD );    // set baudrate to 115200
  dbgSerial.setTimeout( 10 );     // set timeout to 10 msec
  espSerial.begin( ESP_BAUD );    // set baudrate to 115200
  espSerial.setTimeout( 10 );     // set timeout to 10 msec
 
  while (!espSerial) {}
  
  delay(5000);  // wait for a few seconds before continuing
  dbgSerial.println( "Serial ready..." );
  espSerial.flush(); // flush output
  while (espSerial.available()) { espSerial.read(); } // flush incoming input
  
}

int esp8266_transfer( String cmd, uint32_t timeout, boolean verbose=true ) {
  char ch;
  int ret_val = ST_NONE;
  boolean stop = false;
  uint32_t ts;

  espSerial.print( cmd ); // send AT command to ESP8266
  ts = millis();
  while ( (millis() - ts < timeout) && !stop ) {
    while ( espSerial.available() ) {
       ch = espSerial.read(); // read the next byte
       if ( ch == '\n' ) {
          buf[ buf_pos ] = '\0'; // end-of-string (null-terminated)
          buf_pos = 0;
          line = buf;
          if ( verbose ) {
            dbgSerial.print( ">>" );
            dbgSerial.println( line );
          }
          if ( line == "OK" ) {
            ret_val = ST_OK;
          } else if ( line == "ERROR" ) {
            ret_val = ST_ERROR;
          } else if ( line.startsWith("busy") ) {
            ret_val = ST_BUSY;
          } else if ( line == "CLOSED" ) {
            ret_val = ST_CLOSED;
          }       
          if ( ret_val != ST_NONE ) {
            stop = true;
            if ( verbose ) {
               dbgSerial.print( millis() - ts );
               dbgSerial.println( " msec" );
            }
            return ret_val;
          }
       }
       else if ( buf_pos < BUF_SIZE && ch != '\r' ) {
          buf[ buf_pos++ ] = ch;
       }
    }
  }
  line = "";
  buf[ buf_pos ] = '\0';
  buf_pos = 0;
  return ST_NONE;
}

// enable / disable WDT
inline void esp8266_enable_wdt( boolean value ) {
  String cmd = "AT+CSYSWDT";
  cmd += (value) ? "ENABLE" : "DISABLE";
  cmd += "\r\n"; 
  esp8266_transfer( cmd, 1500 );
}

// set WiFi mode
inline void esp8266_set_wifi_mode( int mode ) {
  String cmd = "AT+CWMODE=";
  cmd += mode;    // 1=STA, 2=AP, 3=Both
  cmd += "\r\n"; 
  esp8266_transfer( cmd, 200 );
}

// enable/disable multiple connections
inline void esp8266_use_multiple_connections( boolean value ) {
  String cmd = "AT+CIPMUX=";
  cmd += (value) ? 1 : 0;   // 0=Disable, 1=Enable
  cmd += "\r\n";
  esp8266_transfer( cmd, 200 );
}

inline void esp8266_quit_ap() {
  String cmd = "AT+CWQAP\r\n";  // quit joint AP if any
  esp8266_transfer( cmd, 1000 );
}

inline void esp8266_connect_ap( String ssid, String pass ) {
  String cmd = "AT+CWJAP=\"";
  cmd += ssid;
  cmd += "\",\"";
  cmd += pass;
  cmd += "\"\r\n";
  esp8266_transfer( cmd, 7000 );
}

inline void esp8266_get_joint_ap() {
  String cmd = "AT+CWJAP?\r\n";
  esp8266_transfer( cmd, 500 );
}

inline void esp8266_connect_ap() {
  String cmd;
  //esp8266_quit_ap();
  esp8266_connect_ap( AP_SSID, AP_PASS );
  //esp8266_get_joint_ap(); 
}

inline void esp8266_show_version() {
  String cmd = "AT+GMR\r\n";
  esp8266_transfer( cmd, 500 );
}

inline void esp8266_soft_reset() {
  String cmd = "AT+RST\r\n";
  esp8266_transfer( cmd, 200 );
  delay( 2000 );
  cmd = "AT\r\n";
  if ( esp8266_transfer( cmd, 200 ) != ST_OK ) {
     dbgSerial.println( "Resending AT..");
     delay(1000);
  }
}

void esp8266_init() {
  esp8266_show_version();
  esp8266_enable_wdt( true ); // enable WDT
  esp8266_set_wifi_mode( 1 ); // set WiFi mode to STA
  esp8266_use_multiple_connections( false ); // disable multiple connection
  
}

int esp8266_mysql_update(float realPower1, float realPower2, float realPower3, float realPower4, 
                         float apparentPower1, float apparentPower2, float apparentPower3, float apparentPower4,
                         float Irms1, float Irms2, float Irms3, float Irms4) {
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += SERVER_IP_ADDR;
  cmd += "\",80";
  cmd += "\r\n";
  esp8266_transfer( cmd, 3000 );
  
  String msg;
  msg = "GET /temp/data.php?realPower=";
  msg += String(abs(realPower1));
  msg += "p"+String(abs(realPower2));
  msg += "p"+String(abs(realPower3));
  msg += "p"+String(abs(realPower4));
  
  msg += "&apparentPower=";
  msg += String(abs(apparentPower1));
  msg += "p"+String(abs(apparentPower2));
  msg += "p"+String(abs(apparentPower3));
  msg += "p"+String(abs(apparentPower4));
  
//  msg += "&powerFactor=";
//  msg += String(abs(powerFactor1));
////  msg += "&powerFactor2=";
//  msg += "p"+String(abs(powerFactor2));
////  msg += "&powerFactor3=";
//  msg += "p"+String(abs(powerFactor3));
////  msg += "&powerFactor4=";
//  msg += "p"+String(abs(powerFactor4));

//  msg += "&supplyVoltage1=";
//  msg += supplyVoltage1;
//  msg += "&supplyVoltage2=";
//  msg += supplyVoltage2;
//  msg += "&supplyVoltage3=";
//  msg += supplyVoltage3;
//  msg += "&supplyVoltage4=";
//  msg += supplyVoltage4;

  msg += "&Irms=";
  msg += String(Irms1);

  msg += "p"+String(Irms2);
  msg += "p"+String(Irms3);
  msg += "p"+String(Irms4);

  msg += " HTTP/1.1\r\n";
  msg += "Host: 192.168.0.104\r\n";
  msg += "Connection: Close\r\n";
  msg += "\r\n";

  int num_bytes = msg.length();
  cmd = "AT+CIPSEND=";
  cmd += num_bytes;
  cmd += "\r\n";
  esp8266_transfer( cmd, 2000 );
  
  if ( espSerial.find(">") ){
     int ret = esp8266_transfer( msg, 3000 );
     if ( ret == ST_CLOSED ) {
        return 0; // OK
     }
  } 
  else {
     cmd = "AT+CIPCLOSE\r\n";
     esp8266_transfer( cmd, 2000 );
  }
  return -1; // FAILED
}

  
void loop() {
  esp8266_init();
  uint32_t ts = millis();
  while (1) {
    if ( millis() - ts >= update_interval ) {
      
      ts += update_interval;

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
//      
//      float powerFactor1     = emon1.powerFactor;      //extract Power Factor into Variable
//      float powerFactor2     = emon2.powerFactor;      
//      float powerFactor3     = emon3.powerFactor;      
//      float powerFactor4     = emon4.powerFactor;
//      
//      float supplyVoltage1   = emon1.Vrms;             //extract Vrms into Variable
//      float supplyVoltage2   = emon2.Vrms;
//      float supplyVoltage3   = emon3.Vrms;
//      float supplyVoltage4   = emon4.Vrms;
      
      float Irms1            = emon1.Irms;             //extract Irms into Variable
      float Irms2            = emon2.Irms;             
      float Irms3            = emon3.Irms;             
      float Irms4            = emon4.Irms;
      
      esp8266_connect_ap( AP_SSID, AP_PASS );
      esp8266_mysql_update(realPower1,realPower2,realPower3,realPower4,apparentPower1,apparentPower2,apparentPower3,apparentPower4,Irms1,Irms2,Irms3,Irms4);
     }
  }
}

