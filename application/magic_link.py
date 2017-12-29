from django.test import Client
import json


def send_email(self):
    self.client = Client()
    base_url='http://130.130.52.132:8095'
    header = {'content-type': 'application/json'}
    input = {
        "email": "simulate-delivered@notifications.service.gov.uk",
        "personalisation": {
        "full name":"Name"
    },
        "reference": "string",
        "templateId": "a741fed2-7948-4b1a-b44a-fec8485ec700"
    }
    response = self.client.post('http://130.130.52.132:8095/notify-gateway/api/v1/notifications/email/' , json.dumps(input), 'application/json', header=header)
    print(response.status_code)
    return(response)