#include <ArduinoJson.h>

#include "SerialTransfer.h"


SerialTransfer myTransfer;

struct __attribute__((__packed__)) STRUCT 
{
  bool led_state;
  int some_number;
} workingstruct;

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  if(myTransfer.available())
  {
    myTransfer.rxObj(workingstruct);
    myTransfer.sendDatum(workingstruct);
  }
  digitalWrite(LED_BUILTIN, workingstruct.led_state);
}
