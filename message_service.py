import paho.mqtt.client as mqtt

class MqttMessageService:
    client=mqtt.Client()

    def __init__(self):
        self.client=mqtt.Client()
        
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("imageclassifier/test")

    def on_disconnect(self,client, userdata,rc=0):
        logging.debug("DisConnected result code "+str(rc))
        self.client.loop_stop()
    

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def start_mqtt_service(self,broker,port):
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(broker, port, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        print('loop started')
        self.client.loop_forever()

    def stop_mqtt_service(self):
        self.client.loop_stop()
        print('loop stopped')
