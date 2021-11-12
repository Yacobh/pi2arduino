# pi2arduino
Example code showing implementation of @PowerBroker2's pySerialTransfer and SerialTransfer on both the Python side and Arduino C++ side. 

This example demonstrates sending a bool and a dummy byte from the Python program to the Arduino, receiving and operating on the data with the Arduino in the form of setting an LED, and then sending that same data back over serial, where it is received, processed, and displayed by the Python program.

# Python
```python
import time
from pySerialTransfer import pySerialTransfer as txfer
import json


if __name__ == '__main__':
    try:
        print("iniciamos")
        link = txfer.SerialTransfer('/dev/ttyUSB0')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        ledstate = True
        changetime = time.time()
        senddict = {"ledstate":ledstate}
        while True:
            #check every once in a while to see if it's time to change ledstate     
            if (time.time() - changetime) > 1:
                ledstate = not ledstate
                changetime = time.time()

            send_size = 0
            send_size = link.tx_obj(ledstate, send_size, val_type_override='?')
            send_size = link.tx_obj(234, send_size, val_type_override='B')

            link.send(send_size)
            # wait for reply to be available 
            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))

            rx_struct = {}
            rx_size = 0

            rx_struct['led-state'] = link.rx_obj(obj_type='?', start_pos=rx_size)
            rx_size = txfer.STRUCT_FORMAT_LENGTHS['?']
            rx_struct['some-num'] = link.rx_obj(obj_type='B', start_pos=rx_size)
            rx_size = txfer.STRUCT_FORMAT_LENGTHS['B']

            print(f"ENVIADO DESDE RASPBERRY: {ledstate} and 234.")
            print(f"RECIBIDO DESDE ARDUINO: {rx_struct}")
  
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass
```
# Arduino (C++)
```c++
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
  pinMode(A1, OUTPUT);
}

void loop()
{
  if(myTransfer.available())
  {
    myTransfer.rxObj(workingstruct);
    workingstruct.some_number = 0;
    myTransfer.sendDatum(workingstruct);
  }
  digitalWrite(A1, workingstruct.led_state);
}
```
