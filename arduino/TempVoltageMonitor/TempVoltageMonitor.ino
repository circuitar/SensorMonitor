/*
 Process Monitor
 
 A process monitor for industrial applications. It uploads data to a
 web server using the Ethernet Nanoshield. It reads temperature from
 a type K thermocouple using the Thermocouple Nanoshield and from a
 4-20mA industrial type sensor using the ADC Nanoshield.
 
 Circuit:
 * Base Board Uno
 * Alevino
 * Ethernet Nanoshield
 * Thermocouple Nanoshield
 * ADC Nanoshield

 Copyright (c) 2013 Circuitar
 This software is released under the MIT license. See the attached LICENSE file for details.
 */

#include <SPI.h>
#include <Wire.h>
#include <Ethernet.h>
#include <Nanoshield_EEPROM.h>
#include <Nanoshield_Thermocouple.h>
#include <Adafruit_ADS1015.h>
#include <Nanoshield_RTC.h>

// Macros to convert from float to decimal when using sprintf()
#define POW10(X) (1E##X)
#define DECIMAL(value, places) (int)(value), (int)((value) * POW10(places)) % (int)POW10(places)

// ADC definitions
#define ADC_VREF 6.144

// Peripherals
Nanoshield_EEPROM eeprom(1, 1, 0, true);
Nanoshield_Thermocouple thermocouple;
Adafruit_ADS1115 ads1115;
Nanoshield_RTC rtc;
EthernetClient client;

// Local MAC address
byte mac[6];

// Server IP address
//byte serverIp[] = { 192, 168, 2, 1 }; // Ethernet point-to-point
byte serverIp[] = { 192, 168, 1, 102 }; // Local network
int serverPort = 8000;

// Local IP address
boolean dhcp = true;
//byte localIp[] = { 192, 168, 2, 2 }; // Ethernet point-to-point
byte localIp[] = { 192, 168, 0, 5 }; // Local network

// Buffer to store the POST parameters
char params[100];

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  
  // Read MAC address from EEPROM
  eeprom.begin();
  eeprom.startReading(0x00FA);
  for (int i = 0; i < 6; i++) {
    mac[i] = eeprom.read();
  }

  // Initialize Ethernet
  if (dhcp) {
    Serial.print(F("Attempting DHCP... "));
    if (!Ethernet.begin(mac)) {
      Serial.println(F("Failed"));
    } else {
      Serial.println(F("OK"));
    }
  } else {
    Ethernet.begin(mac, localIp);
  }
  
  // Print connection data
  Serial.print(F("MAC: "));
  Serial.print(mac[0], HEX);
  for (int i = 1; i < 6; i++) { 
    Serial.print(":");
    Serial.print(mac[i], HEX);
  }
  Serial.println();
  Serial.print(F("IP: "));
  Serial.println(Ethernet.localIP());

  // Initialize the ADC
  ads1115.begin();

  // Initialize thermocouple
  thermocouple.begin();

  // Initialize RTC
  rtc.begin();
}

void loop() {
  float intTemp, extTemp, voltage;
  
  // Read thermocouple data
  thermocouple.read();
  
  // Populate variables with sensor data
  intTemp = thermocouple.getInternal();
  extTemp = thermocouple.getExternal();
  voltage = adc2volts(ads1115.readADC_SingleEnded(2), ADC_VREF);
  
  // Prepare POST parameters
  sprintf(params, "int_temp=%d.%01d&ext_temp=%d.%01d&voltage=%d.%02d",
    DECIMAL(intTemp, 1), DECIMAL(extTemp, 1), DECIMAL(voltage, 2));

  // Send data to web server
  if(client.connect(serverIp, serverPort)) {
    // Send HTTP POST
    client.println(F("POST /sensor/ HTTP/1.1"));
    client.print(F("Host: "));
    client.print(serverIp[0]);
    client.print(".");
    client.print(serverIp[1]);
    client.print(".");
    client.print(serverIp[2]);
    client.print(".");
    client.print(serverIp[3]);
    client.print(":");
    client.println(serverPort);
    client.println("User-Agent: Arduino/1.0");
    client.println(F("Connection: close\r\nContent-Type: application/x-www-form-urlencoded"));
    client.print(F("Content-Length: "));
    client.println(strlen(params));
    client.println();
    client.print(params);
    client.stop();
    
    Serial.print(F("Data sent: "));
    Serial.println(params);
  } else {
    Serial.print(F("Unable to connect to server: "));
    Serial.println(params);
  }
  
  delay(800);
}

// Calculate the voltage at the ADC input
float adc2volts(float adc, float vref)
{
  if (adc > 32767) adc = 0;
  return adc * vref / 32767;
}

