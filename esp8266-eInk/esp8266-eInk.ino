#include <ESP8266WiFi.h>
#include <arduino.h>

#include "epd7in5.h"
#include "dataLoader.h"

const char *ssid = "WLAN NAME";
const char *password = "SECRET";
unsigned char connectionSuccess = 30;

unsigned char seg;
String * dataStr;
int delayTime;

void setup()
{
  // Start serial connection at 115200 Baud
  Serial.begin(115200);
  
  // Connect to Wifi
  Serial.print("[WiFi]   Connecting: ");
  while (WiFi.status() != WL_CONNECTED)
  {
    connectionSuccess--;
    if (connectionSuccess == 0) {
      Serial.println(" -> FAILED");
      return;
    }
    delay(500);
    Serial.print(".");
  }
  Serial.println(" --> CONNECTED");

  // DEBUG: print IP over Serial
  Serial.println("");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Mac: ");
  Serial.println(WiFi.macAddress());
  Serial.println("");

}

void loop()
{
  if (connectionSuccess <= 0 || WiFi.status() != WL_CONNECTED) {
    Serial.println("[STATUS] Unconnected --> try restarting");
    delay(5000);
    return;
  }

  // Update the MVG data on the server
  DATA::updateImageData();

  Serial.print("[EPD]    Initialization");
  // Create screen (EPD) instance
  // Initialize / Startup screen
  if (EPD::Init() < 0) {
     Serial.println(" --> FAILED");
     return;
  }
  Serial.println(" --> DONE");

  // Load the image and pass it to screen
  EPD::FrameDataStart();
  seg = 0;
  while (seg < SEG_COUNT) {
    dataStr = DATA::getImageData(seg);
    if ((*dataStr).length() > 0) {
      Serial.println("[STATUS] did update segment " + String(seg) + " out of " + String(SEG_COUNT) + " segments");
      EPD::FrameDataStrBlock(*dataStr);
      seg++;
    } else {
      Serial.println("[STATUS] did NOT update segment " + String(seg) + " out of " + String(SEG_COUNT) + " segments");
      delay(10000);
    }
  }
  EPD::FrameDataStop();
  EPD::FrameDataShow();
  EPD::Sleep();

  delayTime = DATA::getDelayTime();
  Serial.print("[STATUS] waiting " + String(delayTime) + " ms");
  delay(delayTime);
  Serial.println(" --> DONE");
}
