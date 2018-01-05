'''
Created on 5 Jan 2018

@author: Informed Solutions
'''

#Python Imports
import re
import sys
#This style of import should not be standard, and I'll be happy to change on review. This is used to stop its use being too long
import xml.etree.ElementTree as ET

#Django Imports
from django.views.decorators.csrf import csrf_exempt
from test_harness.data_exchange_methods import (SendApplicationForms, GetIndividualsFromSearchCriteria, GetIndividualsRegistrations,
                                                GetIndividualDetails, SendIndividualDetails, GetELSProviderDetails,
                                                GetNewURN, GetReferenceData, SendMessages, GetOrganisationsFromSearchCriteria,
                                                GetOrganisationsDetails, GetInvoiceDetails, SendAdhocPayment, SendPayment,
                                                GetRegistrationFromSearchCriteria, GetRegistrationDetails, SendRegistrationDetails,
                                                error_response)

@csrf_exempt
def NOOHarnessView(request):
    
    #Attempts to pull a valid xml tree out of the request.body byte string (which is in unicode)
    try:
        SOAP_xml = ET.ElementTree(ET.fromstring(request.body))
    except:
        return(error_response('Input format not valid XML!'))
        
    #Assuming format is correct, requested service name, InvokerID, and Parameters can be parsed easily
    #Checks all 
    try:
        SOAP_envelope_node = SOAP_xml.getroot()
        SOAP_body_node = SOAP_envelope_node[0]
        SOAP_service_name_node = SOAP_envelope_node[0][0]
        SOAP_invoker_id_node = SOAP_envelope_node[0][0][0]
        SOAP_parameters_node = SOAP_envelope_node[0][0][1]
        assert(re.sub('{[^>]+}','',(SOAP_envelope_node).tag) == 'Envelope')
        assert(re.sub('{[^>]+}','',(SOAP_body_node).tag) == 'Body')
        assert(type(re.sub('{[^>]+}','',SOAP_service_name_node.tag)) is str )
        assert(type(re.sub('{[^>]+}','',SOAP_invoker_id_node.tag)) is str )
        assert(type(re.sub('{[^>]+}','',SOAP_parameters_node.tag)) is str )
    except AssertionError:
        return(error_response('Request XML in invalid format, consult the web service catalogue'))
    
    except:
        return(error_response('Uncaught error, please contact supporting quoting the following support id' + SOAP_invoker_id_node.text))
    
    
    #Stored in a tuple for easier referencing/passing later
    SOAP_service_name = (re.sub('{[^>]+}','',SOAP_service_name_node.tag))
    print(SOAP_service_name)
    paramater_tuple = (SOAP_invoker_id_node.text, SOAP_parameters_node.text)
   
    #Useful Debugging
    #print(SOAP_result)
    #print(request.body)

    #Dictionary that when queried in the format dict[key](parameters) , will run the function linked with the provided key with
    #the provided parameters
    possible_requests = {'SendApplicationForms': SendApplicationForms,
                         'GetIndividualsFromSearchCriteria': GetIndividualsFromSearchCriteria,
                         'GetIndividualsRegistrations': GetIndividualsRegistrations,
                         'GetIndividualDetails': GetIndividualDetails,
                         'SendIndividualDetails': SendIndividualDetails,
                         'GetELSProviderDetails': GetELSProviderDetails,
                         'GetNewURN': GetNewURN,
                         'GetReferenceData': GetReferenceData,
                         'SendMessages': SendMessages,
                         'GetOrganisationsFromSearchCriteria': GetOrganisationsFromSearchCriteria,
                         'GetOrganisationsDetails': GetOrganisationsDetails,
                         'GetInvoiceDetails': GetInvoiceDetails,
                         'SendAdhocPayment': SendAdhocPayment,
                         'SendPayment': SendPayment,
                         'GetRegistrationFromSearchCriteria': GetRegistrationFromSearchCriteria,
                         'GetRegistrationDetails': GetRegistrationDetails,
                         'SendRegistrationDetails': SendRegistrationDetails      
        }
    
    #If the service found in the request exists, run it's function and return a HttpResponse
    #of an xml string defined in the web service catalogue
    if SOAP_service_name in possible_requests:
        return(possible_requests[SOAP_service_name](paramater_tuple))
    else:
        return(error_response('Requested service does not exist!'))
    
    