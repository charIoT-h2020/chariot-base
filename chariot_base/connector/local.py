import paho.mqtt.client as mqtt

mqtt.Client.connected_flag = False


class LocalConnector(object):
    def __init__(self, client_od, broker):
        self.consumer = mqtt.Client(client_od)
        self.consumer.connect(broker)

        self.consumer.on_log = self.on_log
        self.consumer.on_message = self.on_message

    def on_message(self, client, userdata, message):
        pass

    def on_log(self, client, userdata, level, buf):
        pass

    def subscribe(self, topic):
        self.consumer.subscribe(topic)

    def publish(self, topic, msg):
        self.consumer.publish(topic, msg)

    def start(self, forever=True):
        if forever:
            self.consumer.loop_forever()
        else:
            self.consumer.loop_start()
