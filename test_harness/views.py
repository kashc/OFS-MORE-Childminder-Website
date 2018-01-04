from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4

@csrf_exempt
def NOOHarnessView(request):
    split_body = ((str(request.body)).split('ns0:'))[1]
    result = (split_body.split(' '))[0]
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
    print(result)
    if result in possible_requests:
        return(HttpResponse(possible_requests[result](), content_type = 'text/xml'))
    
    
    
def TestResultView(request):
    pass
    
def SendApplicationForms():
    pass

def GetIndividualsFromSearchCriteria():
    pass

def GetIndividualsRegistrations():
    pass

def GetIndividualDetails():
    pass

def SendIndividualDetails():
    pass

def GetELSProviderDetails():
    return(HttpResponse('''<s12:Envelope xmlns:s12='http://schemas.xmlsoap.org/soap/envelope/'>
  <s12:Body>
    <ns1:GetELSProviderDetails xmlns:ns1='http://127.0.0.1/OfstedOnlineWS'>
      <ns1:GetELSProviderDetailsResult>''' + str(uuid4()) + '''</ns1:GetELSProviderDetailsResult>
    </ns1:GetELSProviderDetails>
  </s12:Body>
</s12:Envelope>''', content_type = 'text/xml'))

def GetNewURN():
    pass

def GetReferenceData():
    pass

def SendMessages():
    pass

def GetOrganisationsFromSearchCriteria():
    pass

def GetOrganisationsDetails():
    pass

def GetInvoiceDetails():
    pass

def SendAdhocPayment():
    pass

def SendPayment():
    pass

def GetRegistrationFromSearchCriteria():
    pass

def GetRegistrationDetails():
    pass

def SendRegistrationDetails():
    pass