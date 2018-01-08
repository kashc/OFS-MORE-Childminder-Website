from django.test import TestCase
import os
from zeep import Client
from base64 import b64decode
import xml.etree.ElementTree as ET

from soapfish import soap, xsd
from test_harness import client, client_schema

wsdl_path = os.path.dirname(__file__)
wsdl_name = os.path.join(wsdl_path, 'OfstedOnlineWS-wsdl.xml')


class OfstedOnlineWSSoapServiceStub(soap.Stub):
    SERVICE = client.OfstedOnlineWSSoap_SERVICE
    SCHEME = 'http'
    HOST = '127.0.0.1:8000'

    def SendApplicationForms(self, SendApplicationForms, header=None):
        return self.call('SendApplicationForms', SendApplicationForms, header=header)

    def GetIndividualsFromSearchCriteria(self, GetIndividualsFromSearchCriteria, header=None):
        return self.call('GetIndividualsFromSearchCriteria', GetIndividualsFromSearchCriteria, header=header)

    def GetIndividualsRegistrations(self, GetIndividualsRegistrations, header=None):
        return self.call('GetIndividualsRegistrations', GetIndividualsRegistrations, header=header)

    def GetIndividualDetails(self, GetIndividualDetails, header=None):
        return self.call('GetIndividualDetails', GetIndividualDetails, header=header)

    def SendIndividualDetails(self, SendIndividualDetails, header=None):
        return self.call('SendIndividualDetails', SendIndividualDetails, header=header)

    def GetELSProviderDetails(self, GetELSProviderDetails, header=None):
        return self.call('GetELSProviderDetails', GetELSProviderDetails, header=header)

    def GetNewURN(self, GetNewURN, header=None):
        return self.call('GetNewURN', GetNewURN, header=header)

    def GetReferenceData(self, GetReferenceData, header=None):
        return self.call('GetReferenceData', GetReferenceData, header=header)

    def SendMessages(self, SendMessages, header=None):
        return self.call('SendMessages', SendMessages, header=header)

    def GetOrganisationsFromSearchCriteria(self, GetOrganisationsFromSearchCriteria, header=None):
        return self.call('GetOrganisationsFromSearchCriteria', GetOrganisationsFromSearchCriteria, header=header)

    def GetOrganisationDetails(self, GetOrganisationDetails, header=None):
        return self.call('GetOrganisationDetails', GetOrganisationDetails, header=header)

    def GetInvoiceDetails(self, GetInvoiceDetails, header=None):
        return self.call('GetInvoiceDetails', GetInvoiceDetails, header=header)

    def SendAdhocPayment(self, SendAdhocPayment, header=None):
        return self.call('SendAdhocPayment', SendAdhocPayment, header=header)

    def SendPayment(self, SendPayment, header=None):
        return self.call('SendPayment', SendPayment, header=header)

    def GetRegistrationsFromSearchCriteria(self, GetRegistrationsFromSearchCriteria, header=None):
        return self.call('GetRegistrationsFromSearchCriteria', GetRegistrationsFromSearchCriteria, header=header)

    def GetRegistrationDetails(self, GetRegistrationDetails, header=None):
        return self.call('GetRegistrationDetails', GetRegistrationDetails, header=header)

    def SendRegistrationDetails(self, SendRegistrationDetails, header=None):
        return self.call('SendRegistrationDetails', SendRegistrationDetails, header=header)



client2 = Client(wsdl_name)
with client2.options(raw_response=True):
    stub = OfstedOnlineWSSoapServiceStub()
    forms = client_schema.SendApplicationForms()
    client_schema.SendApplicationForms.strInvokerID = 'Invoker'
    client_schema.SendApplicationForms.strParameters = 'Params'
    client_schema.SendApplicationForms.strData = 'Data'
    complete = stub.SendApplicationForms(forms)
    print(complete.SendApplicationFormsRes)