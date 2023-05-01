#include <ESP8266HTTPClient.h>

#include <ArduinoWiFiServer.h>
#include <BearSSLHelpers.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiUdp.h>
#include "DHT.h"
#define DHTTYPE DHT11
#include <ArduinoJson.h>
#include <Wire.h>
// #include <Adafruit_BMP085.h>

#include <NTPClient.h>
WiFiUDP ntpUDP;

NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800);

const char* ssid = "Narzo";

const char* password = "qwe123qwe";

DHT dht(0, DHTTYPE);


void setup() {
  Serial.begin(9600);
  // if(!bmp.begin()){
  //   Serial.println("BMP not conntected");
  // }
  // if (!bmp.begin()) {
  //   Serial.println("Could not find a valid BMP180 sensor, check wiring!");
  //   while (1) {}
  // }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");


  dht.begin();
  timeClient.begin();
   while(!timeClient.update()) {
     timeClient.forceUpdate();
   }
//  Serial.end();
}

void send_sensor_data(float temperature, float humidity, float water_level, String formattedTime, int hours, int minutes, int second) {

  HTTPClient http;
  WiFiClient client;
//---------------
//  http.begin(client, "http://127.0.0.1:8000/sensordata/");
//  http.addHeader("Content-Type", "application/json");
//  //-----------

  StaticJsonDocument<2000> jsonDocument;
  jsonDocument["temperature"] = temperature;
  jsonDocument["humidity"] = humidity;
  jsonDocument["water_level"] = water_level;
  jsonDocument["formattedTime"] = formattedTime;
  jsonDocument["hours"] = hours;
  jsonDocument["minutes"] = minutes;
  jsonDocument["seconds"] = second;
  // Serialize the JSON object to a string
  String jsonString;
  serializeJson(jsonDocument, jsonString);
  Serial.println(jsonString);
  //--------------
  int httpResponseCode = http.POST(jsonString);
  if (httpResponseCode == 200) {
    Serial.println("Data sent successfully");
  } else {
    Serial.print("Error sending data. HTTP response code: ");
    Serial.println(httpResponseCode);
  }
  http.end();



}

void loop() {
  timeClient.update();
  float water_level = analogRead(A0);
//  Serial.print("A0 Water_level = ");
//  Serial.println(water_level);


  String formattedTime = timeClient.getFormattedTime();

//  Serial.println(formattedTime);
  int hours = timeClient.getHours();
  int minutes = timeClient.getMinutes();
  int second = timeClient.getSeconds();


  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

//  if (WiFi.status() == WL_CONNECTED) {

  send_sensor_data(temperature, humidity, water_level, formattedTime, hours, minutes, second);
//  }

//  Serial.print("D3 humidity = ");
//  Serial.println(humidity);
  // Serial.print("%  ");
//  Serial.print("D3 temperature = ");
//  Serial.println(temperature);
  // Serial.println(" C");

  delay(3000);

}
