'''
Created on 5 Jan 2018

@author: Informed Solutions
'''
#Python Imports
from uuid import uuid4

#Django Imports
from django.http.response import HttpResponse

#Actual Xml envelope for response content is the same, therefore this has been contained here
def message_response(response_to, content):
    response_to_result = (response_to + 'Result')
    response_string = ('''<s12:Envelope xmlns:s12='http://schemas.xmlsoap.org/soap/envelope/'>
  <s12:Body>
    <ns1:''' + response_to +''' xmlns:ns1='http://127.0.0.1/OfstedOnlineWS'>
        <ns1:'''+ response_to_result + '''>''' + content + '''</ns1:'''+ response_to_result +'''>
    </ns1:'''+ response_to + '''>
  </s12:Body>
</s12:Envelope>''')
    return(response_string)

#Error response is also pre defined in the web service catalogue, needs to be built
def error_response(error):
    return(HttpResponse(error, content_type = 'text/xml'))
    pass

#Each of the below functions will recieve the full xml message sent by the SOAP request, parse it for parameters, then return either
#Of the defined messages to the client

def SendApplicationForms(parameters):
    pass

def GetIndividualsFromSearchCriteria(parameters):
    pass

def GetIndividualsRegistrations(parameters):
    pass

def GetIndividualDetails(parameters):
    pass

def SendIndividualDetails(parameters):
    pass

def GetELSProviderDetails(parameters):
    return(HttpResponse(message_response('GetELSProviderDetails', str(uuid4()))))

def GetNewURN(parameters):
    pass

def GetReferenceData(parameters):
    pass

def SendMessages(parameters):
    pass

def GetOrganisationsFromSearchCriteria(parameters):
    pass

def GetOrganisationsDetails(parameters):
    pass

def GetInvoiceDetails(parameters):
    pass

def SendAdhocPayment(parameters):
    pass

def SendPayment(parameters):
    pass

def GetRegistrationFromSearchCriteria(parameters):
    pass

def GetRegistrationDetails(parameters):
    pass

def SendRegistrationDetails(parameters):
    pass