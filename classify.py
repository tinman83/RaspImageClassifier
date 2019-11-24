import sys
import time
from Daemon import Daemon
from controller import Controller 
from message_service import MqttMessageService

class MyDaemon(Daemon):
    def run(self):
        print('controller running')
        controller = Controller()
        controller.run()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/classify.pid')

    msg_service=MqttMessageService()
    mqttBroker='mqtt.eclipse.org'
    mqttPort=1883
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            msg_service.start_mqtt_service(mqttBroker,mqttPort)
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