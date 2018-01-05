from django.test import TestCase
import os
from zeep import Client

wsdl_path = os.path.dirname(__file__)
wsdl_name = os.path.join(wsdl_path, 'OfstedOnlineWS-wsdl.xml')

client = Client(wsdl_name)
print(client.service.GetELSProviderDetails(24,'www'))
