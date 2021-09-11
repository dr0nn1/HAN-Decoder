# Importing packages
import six
import os
import serial
import logging
import paho.mqtt.client as mqtt
from hanDecoding import hanDecoding
from influxWriter import writeToInflux
from curtime import curtime

def on_log(client,userdata,level,buf):
        print("log: "+ buf)

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect code: ",rc)

broker_address="192.168.0.51" 
client = mqtt.Client("ams")
#client.username_pw_set(username="user",password="pw")
client.on_connect=on_connect
client.on_log=on_log
client.on_disconnect = on_disconnect
client.connect(broker_address)
client.loop_start()

# Logging utility

logging.basicConfig(filename='debuglog.txt', level=os.environ.get('LOGLEVEL', 'DEBUG'))
log = logging.getLogger('Power Meter')

# Converts given bytestring to hexstring
bytes_to_hex = lambda incoming_bytes: ' '.join('%02x' % b for b in six.iterbytes(incoming_bytes)).upper()

# Connecting to serial
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=2400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=4)

print(f'Connected to: {ser.portstr}')
oldbytes = ""
# Receives data
while True:
#    try:
        incoming_bytes = ser.read(1024)
        if incoming_bytes:
            now = curtime()
            log.debug(now)
            log.debug(f'Received {len(incoming_bytes)}')
            incoming_as_hex = bytes_to_hex(incoming_bytes)
            log.debug(incoming_as_hex)
            now = curtime()
            lastElement = int(incoming_as_hex[-2:],16)
            firstElement = int(incoming_as_hex[:2],16)

            if (lastElement != int('7E',16)):
                if not oldbytes:
                    oldbytes= incoming_as_hex + " "
                else:
                    oldbytes = oldbytes + incoming_as_hex + " "
            elif firstElement != int('7E',16):
                incoming_as_hex = oldbytes + incoming_as_hex
                oldbytes=""
            elif len(incoming_bytes) == 1 and  incoming_as_hex == int('7E',16) and len(oldbytes) > 0:
                incoming_as_hex = oldbytes + incoming_as_hex
                oldbytes=""
            elif len(incoming_bytes) == 1 and  incoming_as_hex == int('7E',16) and len(oldbytes) == 0:
                oldbytes= incoming_as_hex + " "
            else:
                oldbytes=""

            if len(incoming_as_hex) < 683:
                log.debug(f'bytes < 228')
            elif not oldbytes:
                jsonvalues = hanDecoding(incoming_as_hex)
                writeToInflux(jsonvalues)
                client.publish("ams",jsonvalues)
#    except Exception:
#        log.error('Exception')
#        pass
