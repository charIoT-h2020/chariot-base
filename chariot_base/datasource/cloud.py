import json

from cloudant import Cloudant
from datetime import datetime

OPTS = {
  "apikey": "yP_EXGzI1MhmTzrIKHT4JKWUldjV1TTRDm1wSQiXHEhq",
  "host": "a1c81012-ed4f-4203-b6e7-bdb24f3cfd36-bluemix.cloudant.com",
  "iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:cloudantnosqldb:eu-gb:a/69e682b4b607c70e26ba1bbfc0ed1ed4:44ebc1b6-8694-46b8-b4f8-69730bf2810c::",
  "iam_apikey_name": "auto-generated-apikey-66b42435-9415-438a-af1c-4fea44400908",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/69e682b4b607c70e26ba1bbfc0ed1ed4::serviceid:ServiceId-66e7265d-82c5-483c-9d1d-123480822656",
  "password": "40b52723334e54309b268fec64ab0fe85012866eaddefd040035d74888bfe47f",
  "port": 443,
  "url": "https://a1c81012-ed4f-4203-b6e7-bdb24f3cfd36-bluemix:40b52723334e54309b268fec64ab0fe85012866eaddefd040035d74888bfe47f@a1c81012-ed4f-4203-b6e7-bdb24f3cfd36-bluemix.cloudant.com",
  "username": "a1c81012-ed4f-4203-b6e7-bdb24f3cfd36-bluemix"
}


class DataSource(object):

    def __init__(self):
        self.my_database = None
        self.cloudant_client = Cloudant(OPTS['username'], OPTS['password'],
                                        account=OPTS['account'], connect=True)

    def get_last(self, gateway, sensor):
        """
        Gets the last reading of a sensor in a gateway from Cloudant.
        :param gateway: name of the gateway
        :param sensor: name of the sensor
        :return: timestamp and value in json format.
        """
        current_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        self.my_database = self.cloudant_client['iotp_3yfv6b_default_{}'.format(current_date)]
        selector = dict(eventType={'$eq': '{}.sensor'.format(sensor)},
                        deviceType={'$eq': gateway},
                        _id={'$gt': 0})
        result_collection = self.my_database.get_query_result(selector,
                                                              fields=['data'], sort=[{'_id': 'desc'}], limit=1)
        if result_collection:
            return result_collection[0][0]['data']
        else:
            return None


def main():
    d = DataSource()
    print(d.get_last('temperature'))
    print(d.get_last('humidity'))


if __name__ == '__main__':
    main()
