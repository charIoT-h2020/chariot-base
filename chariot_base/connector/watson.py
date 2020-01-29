from multiprocessing import Process

import wiotp.sdk.device


class WatsonConnector(Process):

    def __init__(self, options):
        super(WatsonConnector, self).__init__()
        try:
            self.iot_client = wiotp.sdk.device.DeviceClient(config=options, logHandlers=None)
            self.iot_client.connect()
        except Exception as e:
            print(e)

    def publish(self, point):
        """
        :param point: A point represent received message.
        :return: True if event publish is successfull.
        """
        return self.iot_client.publishEvent(eventId=point.table, msgFormat="json", data=point.message, qos=0, onPublish=None)
