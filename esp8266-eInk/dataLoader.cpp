#include "dataLoader.h"

namespace DATA {
  
  String dataStr;
  
  void getHttpData(String url) {
    WiFiClient c;
    HTTPClient http;
    
    if (http.begin(c, url)) {
      Serial.print("[DATA]   sending HTTP-GET");
      int httpCode = http.GET();
      Serial.println(" --> DONE");

      if (httpCode == HTTP_CODE_OK) {
          Serial.print("[DATA]   getting data (");
          Serial.print(http.getSize());
          Serial.print(")");
          dataStr = http.getString();
          Serial.println(" --> DONE");
      } else {
        Serial.println("[DATA]   No data received from \"" + url + "\"");
        Serial.println("[DATA]   Response code was: " + String(httpCode));
      }

      http.end();
    } else  {
      Serial.println("[HTTP]   unable to connect to server");
    }
  }

  int updateImageData() {
    getHttpData(DATA_URL + "/update/" + WiFi.macAddress());
    return dataStr.toInt();
  }
  
  String * getImageData(unsigned char seg) {
    getHttpData(DATA_URL + "/imageData/" + WiFi.macAddress() + "?segCount=" + String(SEG_COUNT) + "&seg=" + String(seg));
    return &dataStr;
  }
  
  int getDelayTime() {
    getHttpData(DATA_URL + "/delayTime/" + WiFi.macAddress());
    return dataStr.toInt();
  }
}
