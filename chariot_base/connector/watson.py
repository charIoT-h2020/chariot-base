from multiprocessing import Process

import ibmiotf.gateway


class WatsonConnector(Process):

    def __init__(self):
        super(WatsonConnector, self).__init__()
        try:
            options = {
                "org": "jv8w5u",
                "type": "gateway",
                "id": "5410ec4d1601",
                "auth-method": "token",
                "auth-token": "Mw35yK?VRvsb-Qqjy3"
            }
            self.iot_client = ibmiotf.gateway.Client(options)
            self.iot_client.connect()
        except ibmiotf.ConnectionException as e:
            print(e)

    def publish(self, point):
        """
        :param point: point
        :return:
        """
        self.iot_client.publishGatewayEvent(event=point.table, msgFormat="json", data=point.message)

