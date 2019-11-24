import sys
import time
import logging
import threading
from Daemon import Daemon
from controller import Controller 
from message_service import MqttMessageService

class MyDaemon(Daemon):

    def run(self):
        # print(self.flags.getPredictFlag())
        print('controller running')
        controller = Controller()
        controller.run()

msg_service=MqttMessageService()
def mqtt_Service_Start_Thread(args):
    mqttBroker=args[0]
    mqttPort=args[1]

    msg_service=MqttMessageService()

    msg_service.start_mqtt_service(mqttBroker,mqttPort)

if __name__ == "__main__":
    mqttBroker='mqtt.eclipse.org'
    mqttPort=1883
    
    daemon = MyDaemon('/tmp/classify.pid')
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:

            # mqtt_args = [mqttBroker,mqttPort]
            # mqtt_thread = threading.Thread(target=mqtt_Service_Start_Thread, args=(mqtt_args,))
            # mqtt_thread.start()
            msg_service.start_mqtt_service(mqttBroker,mqttPort)
            print("Thread started")

            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            msg_service.stop_mqtt_service()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'reconnect_mqtt' == sys.argv[1]:
            msg_service.start_mqtt_service(mqttBroker,mqttPort)
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)