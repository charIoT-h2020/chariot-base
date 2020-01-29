from cloudant import Cloudant
from datetime import datetime


class CloudDataSource(object):

    def __init__(self, options):
        self.my_database = None
        self.orgId = options['orgId']
        self.cloudant_client = Cloudant.iam(options['username'], options['apikey'], connect=True)

    def get_last(self, device_type, device_id=None):
        """
        Gets the last reading of a sensor in a gateway from Cloudant.
        :param device_type: name of the gateway
        :param device_id: name of the sensor
        :return: timestamp and value in json format.
        """
        self.my_database = self.cloudant_client['chariot-raw-message']

        if device_id is None:
            selector = dict(eventType='message',
                            deviceType={'$eq': device_type},
                            _id={'$gt': 0})
        else:
            selector = dict(deviceId=device_id,
                            deviceType={'$eq': device_type},
                            _id={'$gt': 0})

        result_collection = self.my_database.get_query_result(selector,
                                                              fields=['payload'], sort=[{'_id': 'desc'}], limit=1)

        print(result_collection)
        if len(result_collection[:]) > 0:
            return result_collection[0][0]['payload']
        else:
            return None

    def get_all_database(self):
        return self.cloudant_client.all_dbs()
