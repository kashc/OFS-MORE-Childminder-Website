'''
Created on 5 Jan 2018

@author: Informed Solutions
'''
#Python Imports
from uuid import uuid4
from base64 import b64encode, b64decode

#Django Imports
from django.http.response import HttpResponse

#Actual Xml envelope for response content is the same, therefore this has been contained here
def message_response( status, response_to = '', error = ''):
    result_string = (response_to + 'Result')
    payload_string = b64encode(b"""<Status>"""+ status.encode('utf-8') +b"""</Status>
<InvocationID>"""+ response_to.encode('utf-8') +b"""</InvocationID>
<Error>"""+ error.encode('utf-8') +b"""</Error>""")
    response_string = ("""<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <"""+ result_string +""">"""+ str(payload_string) +"""</"""+ result_string +""">
    </soap:Body>
</soap:Envelope>""")
    print(response_string)
    return(response_string)

#Error response is also pre defined in the web service catalogue, needs to be built
def error_response(error):
    return(HttpResponse(error, content_type = 'text/xml'))
    pass

#Each of the below functions will recieve the full xml message sent by the SOAP request, parse it for parameters, then return either
#Of the defined messages to the client

def SendApplicationForms(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetIndividualsFromSearchCriteria(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetIndividualsRegistrations(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetIndividualDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def SendIndividualDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetELSProviderDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetNewURN(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetReferenceData(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def SendMessages(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetOrganisationsFromSearchCriteria(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetOrganisationsDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetInvoiceDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def SendAdhocPayment(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def SendPayment(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetRegistrationFromSearchCriteria(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def GetRegistrationDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))

def SendRegistrationDetails(service_name, invoker_id, parameters_xml):
    SUCCESS = '0'
    FAILURE = '1'
    #any parameter parsing/processing should go here
    return(message_response(SUCCESS, service_name))