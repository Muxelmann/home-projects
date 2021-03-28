#include <arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#ifndef DATALOADER_H
#define DATALOADER_H

#define DATA_URL String("http://192.168.5.241/mvg-frame")
// #define DATA_URL String("http://192.168.5.201:5000/mvg-frame")
#define SEG_COUNT 6


namespace DATA {

  void getHttpData(String url);

  int updateImageData();
  
  String * getImageData(unsigned char seg);
  
  int getDelayTime();
  
}

#endif /* DATALOADER_H */
