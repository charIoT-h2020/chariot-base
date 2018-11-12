from multiprocessing import Process

import ibmiotf.gateway


class WatsonConnector(Process):

    def __init__(self, options):
        super(WatsonConnector, self).__init__()
        try:
            self.iot_client = ibmiotf.gateway.Client(options)
            self.iot_client.connect()
        except ibmiotf.ConnectionException as e:
            print(e)

    def publish(self, point):
        """
        :param point: point
        :return:
        """
        return self.iot_client.publishGatewayEvent(event=point.table, msgFormat="json", data=point.message)
