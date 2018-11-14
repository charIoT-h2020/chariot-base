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
        current_date = datetime.strftime(datetime.now(), '%Y-%m-%d')  # 2018-11-10
        self.my_database = self.cloudant_client['iotp_%s_default_%s' % (self.orgId, current_date)]

        if device_id is None:
            selector = dict(eventType='message',
                            deviceType={'$eq': device_type},
                            _id={'$gt': 0})
        else:
            selector = dict(deviceId=device_id,
                            deviceType={'$eq': device_type},
                            _id={'$gt': 0})

        result_collection = self.my_database.get_query_result(selector,
                                                              fields=['data'], sort=[{'_id': 'desc'}], limit=1)
        if len(result_collection[:]) > 0:
            return result_collection[0][0]['data']
        else:
            return None

    def get_all_database(self):
        return self.cloudant_client.all_dbs()
