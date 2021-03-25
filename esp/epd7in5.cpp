#include "epd7in5.h"

namespace EPD {
  int isSetup = -1;

  int Init(void) {
    if (InterfaceSetup() < 0) {
      return -1;
    }
    InterfaceReset();
  
    SendCommand(POWER_SETTING);
    SendData(0x37);
    SendData(0x00);
  
    SendCommand(PANEL_SETTING);
    SendData(0xCF);
    SendData(0x08);
  
    SendCommand(BOOSTER_SOFT_START);
    SendData(0xc7);
    SendData(0xcc);
    SendData(0x28);
  
    SendCommand(POWER_ON);
    WaitUntilIdle();
  
    SendCommand(PLL_CONTROL);
    SendData(0x3c);
  
    SendCommand(TEMPERATURE_CALIBRATION);
    SendData(0x00);
  
    SendCommand(VCOM_AND_DATA_INTERVAL_SETTING);
    SendData(0x77);
  
    SendCommand(TCON_SETTING);
    SendData(0x22);
  
    SendCommand(TCON_RESOLUTION);
    SendData(0x02);     //source 640
    SendData(0x80);
    SendData(0x01);     //gate 384
    SendData(0x80);
  
    SendCommand(VCM_DC_SETTING);
    SendData(0x1e);      //decide by LUT file
  
    SendCommand(FLASH_MODE);
    SendData(0x03);
  
    return 0;
  }

  int InterfaceSetup(void) {
    if (isSetup < 0) {
      pinMode(CS_PIN, OUTPUT);
      pinMode(RST_PIN, OUTPUT);
      pinMode(DC_PIN, OUTPUT);
      pinMode(BUSY_PIN, INPUT);
  
      SPI.begin();
      SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE0));
      isSetup = 0;
    }
    return isSetup;
  }
  
  void InterfaceReset(void) {
    digitalWrite(RST_PIN, LOW);                //module reset
    delay(200);
    digitalWrite(RST_PIN, HIGH);
    delay(200);
  }
  
  void SpiTransfer(unsigned char data) {
    digitalWrite(CS_PIN, LOW);
    SPI.transfer(data);
    digitalWrite(CS_PIN, HIGH);
  }
  
  void SendCommand(unsigned char command) {
    digitalWrite(DC_PIN, LOW);
    SpiTransfer(command);
  }
  
  void SendData(unsigned char data) {
    digitalWrite(DC_PIN, HIGH);
    SpiTransfer(data);
  }
  
  void WaitUntilIdle(void) {
    while (digitalRead(BUSY_PIN) == 0) {     //0: busy, 1: idle
      delay(100);
    }
  }
  
  void FrameDataStart(void) {
    SendCommand(0x10);
  }
  
  void FrameDataStop(void) {
    SendCommand(0x11);
  }
  
  void FrameDataShow(void) {
    // Refresh display
    SendCommand(0x12);
    delay(100);
    WaitUntilIdle();
  
    // Sleep
    SendCommand(0x02);  // Power off
    WaitUntilIdle();
    SendCommand(0x07);
    SendData(0xA5);     // Deep sleep
  }
  
  void FrameDataClear(void) {
    int doublePixels = (EPD_WIDTH * EPD_HEIGHT) >> 1;
    for (int p = 0; p < doublePixels; p++) {
      SendData(0x33);
    }
  }
  
  void Sleep(void) {
    SendCommand(POWER_OFF);
    WaitUntilIdle();
    SendCommand(DEEP_SLEEP);
    SendData(0xa5);
  }

  void FrameDataStrBlock(String dataStr) {
    /* EPD takes 4 bit per pixel, which encodes colors as follows
     * 0b0000 --> black
     * 0b0011 --> white
     * 0b0100 --> color (red or yellow)
     * 
     * In the past I decoded a string of hex values, based on whether color is available.
     * Later, I encoded 2 bit per pixel and used the same ESP code regardless whether color is available:
     * 0b00 --> black
     * 0b01 --> color
     * 0b10 --> color
     * 0b11 --> white
     * 
     * To reduce TX-data, I combined data for 2 pixels into one hex value, e.g.: 
     *     black, black, white, black
     * --> 0b00   0b00   0b11   0b00
     * --> 0x0           0xc          --> 0x0c
     * 
     * This is still applied here for legacy reasons...
     */

    const char* data = dataStr.c_str();
    unsigned int dataLen = dataStr.length();
  
    for (unsigned int ptr = 0; ptr < dataLen; ptr++) {
      switch (data[ptr]) {
        case '0': SendData(COLOR_BLACK << 4 | COLOR_BLACK); break;
        case '1': SendData(COLOR_BLACK << 4 | COLOR_RED); break;
        case '2': SendData(COLOR_BLACK << 4 | COLOR_RED); break;
        case '3': SendData(COLOR_BLACK << 4 | COLOR_WHITE); break;
        case '4': SendData(COLOR_RED   << 4 | COLOR_BLACK); break;
        case '5': SendData(COLOR_RED   << 4 | COLOR_RED); break;
        case '6': SendData(COLOR_RED   << 4 | COLOR_RED); break;
        case '7': SendData(COLOR_RED   << 4 | COLOR_WHITE); break;
        case '8': SendData(COLOR_RED   << 4 | COLOR_BLACK); break;
        case '9': SendData(COLOR_RED   << 4 | COLOR_RED); break;
        case 'a': SendData(COLOR_RED   << 4 | COLOR_RED); break;
        case 'b': SendData(COLOR_RED   << 4 | COLOR_WHITE); break;
        case 'c': SendData(COLOR_WHITE << 4 | COLOR_BLACK); break;
        case 'd': SendData(COLOR_WHITE << 4 | COLOR_RED); break;
        case 'e': SendData(COLOR_WHITE << 4 | COLOR_RED); break;
        case 'f': SendData(COLOR_WHITE << 4 | COLOR_WHITE); break;
        default:  SendData(COLOR_BLACK << 4 | COLOR_BLACK); break;
      }
    }
  }

  /*
  void FrameBufferDisplay(unsigned char * frameBuffer, unsigned long bufferLength) {
    // Only works for black and white
    unsigned char buf_in, buf_out;

    for (unsigned long i = 0; i < bufferLength; i++) {
      buf_in = pgm_read_byte(&frameBuffer[i]);
      for (unsigned char j = 0; j < 4; j++) {
        // set data based on 1st bit and 2nd bit
        buf_out =  buf_in & 0x80 ? 0x30 : 0x00;
        buf_out |= buf_in & 0x40 ? 0x03 : 0x00;

        // send data for the 2 bits
        SendData(buf_out);
        
        // shift by 2 bits
        buf_in <<= 2;
      }
    }
  }
  */

}
