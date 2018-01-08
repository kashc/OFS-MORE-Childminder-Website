'''
Created on 8 Jan 2018

@author: geevesh
'''
from soapfish import soap, xsd
from .client_schema import Schema_574e8

BaseHeader = xsd.ComplexType


##############################################################################
# Methods


SendApplicationForms_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendApplicationForms',
    input='SendApplicationForms',
    inputPartName='parameters',
    output='SendApplicationFormsResponse',
    outputPartName='parameters',
    operationName='SendApplicationForms',
    style='document',
)


GetIndividualsFromSearchCriteria_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetIndividualsFromSearchCriteria',
    input='GetIndividualsFromSearchCriteria',
    inputPartName='parameters',
    output='GetIndividualsFromSearchCriteriaResponse',
    outputPartName='parameters',
    operationName='GetIndividualsFromSearchCriteria',
    style='document',
)


GetIndividualsRegistrations_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetIndividualsRegistrations',
    input='GetIndividualsRegistrations',
    inputPartName='parameters',
    output='GetIndividualsRegistrationsResponse',
    outputPartName='parameters',
    operationName='GetIndividualsRegistrations',
    style='document',
)


GetIndividualDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetIndividualDetails',
    input='GetIndividualDetails',
    inputPartName='parameters',
    output='GetIndividualDetailsResponse',
    outputPartName='parameters',
    operationName='GetIndividualDetails',
    style='document',
)


SendIndividualDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendIndividualDetails',
    input='SendIndividualDetails',
    inputPartName='parameters',
    output='SendIndividualDetailsResponse',
    outputPartName='parameters',
    operationName='SendIndividualDetails',
    style='document',
)


GetELSProviderDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetELSProviderDetails',
    input='GetELSProviderDetails',
    inputPartName='parameters',
    output='GetELSProviderDetailsResponse',
    outputPartName='parameters',
    operationName='GetELSProviderDetails',
    style='document',
)


GetNewURN_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetNewURN',
    input='GetNewURN',
    inputPartName='parameters',
    output='GetNewURNResponse',
    outputPartName='parameters',
    operationName='GetNewURN',
    style='document',
)


GetReferenceData_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetReferenceData',
    input='GetReferenceData',
    inputPartName='parameters',
    output='GetReferenceDataResponse',
    outputPartName='parameters',
    operationName='GetReferenceData',
    style='document',
)


SendMessages_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendMessages',
    input='SendMessages',
    inputPartName='parameters',
    output='SendMessagesResponse',
    outputPartName='parameters',
    operationName='SendMessages',
    style='document',
)


GetOrganisationsFromSearchCriteria_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetOrganisationsFromSearchCriteria',
    input='GetOrganisationsFromSearchCriteria',
    inputPartName='parameters',
    output='GetOrganisationsFromSearchCriteriaResponse',
    outputPartName='parameters',
    operationName='GetOrganisationsFromSearchCriteria',
    style='document',
)


GetOrganisationDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetOrganisationDetails',
    input='GetOrganisationDetails',
    inputPartName='parameters',
    output='GetOrganisationDetailsResponse',
    outputPartName='parameters',
    operationName='GetOrganisationDetails',
    style='document',
)


GetInvoiceDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetInvoiceDetails',
    input='GetInvoiceDetails',
    inputPartName='parameters',
    output='GetInvoiceDetailsResponse',
    outputPartName='parameters',
    operationName='GetInvoiceDetails',
    style='document',
)


SendAdhocPayment_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendAdhocPayment',
    input='SendAdhocPayment',
    inputPartName='parameters',
    output='SendAdhocPaymentResponse',
    outputPartName='parameters',
    operationName='SendAdhocPayment',
    style='document',
)


SendPayment_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendPayment',
    input='SendPayment',
    inputPartName='parameters',
    output='SendPaymentResponse',
    outputPartName='parameters',
    operationName='SendPayment',
    style='document',
)


GetRegistrationsFromSearchCriteria_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetRegistrationsFromSearchCriteria',
    input='GetRegistrationsFromSearchCriteria',
    inputPartName='parameters',
    output='GetRegistrationsFromSearchCriteriaResponse',
    outputPartName='parameters',
    operationName='GetRegistrationsFromSearchCriteria',
    style='document',
)


GetRegistrationDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/GetRegistrationDetails',
    input='GetRegistrationDetails',
    inputPartName='parameters',
    output='GetRegistrationDetailsResponse',
    outputPartName='parameters',
    operationName='GetRegistrationDetails',
    style='document',
)


SendRegistrationDetails_method = xsd.Method(
    soapAction='http://127.0.0.1/OfstedOnlineWS/SendRegistrationDetails',
    input='SendRegistrationDetails',
    inputPartName='parameters',
    output='SendRegistrationDetailsResponse',
    outputPartName='parameters',
    operationName='SendRegistrationDetails',
    style='document',
)

##############################################################################
# SOAP Service


OfstedOnlineWSSoap_SERVICE = soap.Service(
    name='OfstedOnlineWSSoap',
    targetNamespace='http://127.0.0.1/OfstedOnlineWS',
    location='${scheme}://${host}/OfstedOnlineWS/',
    schemas=[Schema_574e8],
    version=soap.SOAPVersion.SOAP12,
    methods=[SendApplicationForms_method, GetIndividualsFromSearchCriteria_method, GetIndividualsRegistrations_method, GetIndividualDetails_method, SendIndividualDetails_method, GetELSProviderDetails_method, GetNewURN_method, GetReferenceData_method, SendMessages_method, GetOrganisationsFromSearchCriteria_method, GetOrganisationDetails_method, GetInvoiceDetails_method, SendAdhocPayment_method, SendPayment_method, GetRegistrationsFromSearchCriteria_method, GetRegistrationDetails_method, SendRegistrationDetails_method],
)


##############################################################################
