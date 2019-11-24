import sys
import time
import paho.mqtt.client as mqtt

class MqttMessageService:
    client=mqtt.Client()
    Connected = False

    def __init__(self):
        self.client=mqtt.Client()

    def on_connect(self,client, userdata, flags, rc):
         print("Connected with result code "+str(rc))
         global Connected
         Connected=True
 
         try:
            r=self.client.subscribe("imageclassifier/test")
            if r[0]==0:
                print("subscribed to topic ") 
            else:
                 print("error on subscribing " + str(r))
                 self.client.loop_stop()
                 sys.exit(1)
         except Exception as e:
            print("error on subscribe " + str(e))
            self.client.loop_stop()
            sys.exit(1)
         

    def on_disconnect(self,client, userdata,rc=0):
        print("DisConnected result code "+str(rc))
        global Connected
        Connected = False
        self.client.loop_stop()
    

    def on_message(self,client, userdata, msg):
        print("Message Received")
        print(msg.topic+" "+str(msg.payload))
        self.flags.setPredictFlag(True)

    def start_mqtt_service(self,broker,port):
        global Connected
        Connected = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        try:
            self.client.connect(broker, port=port)
        except:
            print("cannot connect")
            sys.exit(1)

        print('loop started')
        self.client.loop_start()
        while Connected != True:
            print("waiting to connect")
            time.sleep(0.1)

    def stop_mqtt_service(self):
        self.client.loop_stop()
        print('loop stopped')
