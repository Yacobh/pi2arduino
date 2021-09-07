import time
from pySerialTransfer import pySerialTransfer as txfer
import json


if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('/dev/ttyACM0')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        ledstate = True
        changetime = time.time()
        senddict = {"ledstate":ledstate}
        while True:
            #check every once in a while to see if it's time to change ledstate
            if (time.time() - changetime) > .5:
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
            rx_size += txfer.STRUCT_FORMAT_LENGTHS['?']
            rx_struct['some-num'] = link.rx_obj(obj_type='B', start_pos=rx_size)
            rx_size += txfer.STRUCT_FORMAT_LENGTHS['B']

            print(f"Sent: {ledstate} and 12345.")
            print(f"Got a reply: {rx_struct}")
            

            
            
            
    
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
