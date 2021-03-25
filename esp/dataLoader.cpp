#include "dataLoader.h"

namespace DATA {
  
  String getHttpData(String url) {
    WiFiClient c;
    HTTPClient http;
    String httpData;
    
    if (http.begin(c, url)) {
      Serial.print("[DATA] sending HTTP-GET");
      int httpCode = http.GET();
      Serial.println(" --> DONE");

      if (httpCode == HTTP_CODE_OK) {
          httpData = http.getString();
      } else {
        Serial.println("[DATA] No data received from \"" + url + "\"");
        Serial.println("[DATA] Response code was: " + String(httpCode));
      }

      http.end();
    } else  {
      Serial.println("[HTTP] unable to connect to server");
    }
  
    return httpData;
  }

  int updateImageData() {
    return getHttpData(DATA_URL + "/update/" + WiFi.macAddress()).toInt();
  }
  
  String getImageData(unsigned char seg) {
    return getHttpData(DATA_URL + "/imageData/" + WiFi.macAddress() + "&segCount=" + String(SEG_COUNT) + "&seg=" + String(seg));
  }
  
  int getDelayTime() {
    return getHttpData(DATA_URL + "/delayTime/" + WiFi.macAddress()).toInt();
  }
}
