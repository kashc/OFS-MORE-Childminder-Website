'''
Created on 8 Jan 2018

@author: geevesh
'''
from soapfish import xsd

BaseHeader = xsd.ComplexType

##############################################################################
# Schemas


# http://127.0.0.1/OfstedOnlineWS


class SendApplicationForms(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendApplicationFormsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendApplicationFormsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualsFromSearchCriteria(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualsFromSearchCriteriaResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetIndividualsFromSearchCriteriaResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualsRegistrations(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualsRegistrationsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetIndividualsRegistrationsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetIndividualDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetIndividualDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendIndividualDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendIndividualDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendIndividualDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetELSProviderDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetELSProviderDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetELSProviderDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetNewURN(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetNewURNResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetNewURNResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetReferenceData(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetReferenceDataResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetReferenceDataResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendMessages(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendMessagesResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendMessagesResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetOrganisationsFromSearchCriteria(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetOrganisationsFromSearchCriteriaResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetOrganisationsFromSearchCriteriaResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetOrganisationDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetOrganisationDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetOrganisationDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetInvoiceDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetInvoiceDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetInvoiceDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendAdhocPayment(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendAdhocPaymentResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendAdhocPaymentResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendPayment(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendPaymentResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendPaymentResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetRegistrationsFromSearchCriteria(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetRegistrationsFromSearchCriteriaResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetRegistrationsFromSearchCriteriaResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetRegistrationDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class GetRegistrationDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    GetRegistrationDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendRegistrationDetails(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    strInvokerID = xsd.Element(xsd.String, minOccurs=0)
    strParameters = xsd.Element(xsd.String, minOccurs=0)
    strData = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


class SendRegistrationDetailsResponse(xsd.ComplexType):
    INHERITANCE = None
    INDICATOR = xsd.Sequence
    SendRegistrationDetailsResult = xsd.Element(xsd.String, minOccurs=0)

    @classmethod
    def create(cls):
        instance = cls()
        return instance


Schema_574e8 = xsd.Schema(
    imports=[],
    includes=[],
    targetNamespace='http://127.0.0.1/OfstedOnlineWS',
    elementFormDefault='qualified',
    simpleTypes=[],
    attributeGroups=[],
    groups=[],
    complexTypes=[],
    elements={'SendApplicationForms': xsd.Element(SendApplicationForms()), 'SendApplicationFormsResponse': xsd.Element(SendApplicationFormsResponse()), 'GetIndividualsFromSearchCriteria': xsd.Element(GetIndividualsFromSearchCriteria()), 'GetIndividualsFromSearchCriteriaResponse': xsd.Element(GetIndividualsFromSearchCriteriaResponse()), 'GetIndividualsRegistrations': xsd.Element(GetIndividualsRegistrations()), 'GetIndividualsRegistrationsResponse': xsd.Element(GetIndividualsRegistrationsResponse()), 'GetIndividualDetails': xsd.Element(GetIndividualDetails()), 'GetIndividualDetailsResponse': xsd.Element(GetIndividualDetailsResponse()), 'SendIndividualDetails': xsd.Element(SendIndividualDetails()), 'SendIndividualDetailsResponse': xsd.Element(SendIndividualDetailsResponse()), 'GetELSProviderDetails': xsd.Element(GetELSProviderDetails()), 'GetELSProviderDetailsResponse': xsd.Element(GetELSProviderDetailsResponse()), 'GetNewURN': xsd.Element(GetNewURN()), 'GetNewURNResponse': xsd.Element(GetNewURNResponse()), 'GetReferenceData': xsd.Element(GetReferenceData()), 'GetReferenceDataResponse': xsd.Element(GetReferenceDataResponse()), 'SendMessages': xsd.Element(SendMessages()), 'SendMessagesResponse': xsd.Element(SendMessagesResponse()), 'GetOrganisationsFromSearchCriteria': xsd.Element(GetOrganisationsFromSearchCriteria()), 'GetOrganisationsFromSearchCriteriaResponse': xsd.Element(GetOrganisationsFromSearchCriteriaResponse()), 'GetOrganisationDetails': xsd.Element(GetOrganisationDetails()), 'GetOrganisationDetailsResponse': xsd.Element(GetOrganisationDetailsResponse()), 'GetInvoiceDetails': xsd.Element(GetInvoiceDetails()), 'GetInvoiceDetailsResponse': xsd.Element(GetInvoiceDetailsResponse()), 'SendAdhocPayment': xsd.Element(SendAdhocPayment()), 'SendAdhocPaymentResponse': xsd.Element(SendAdhocPaymentResponse()), 'SendPayment': xsd.Element(SendPayment()), 'SendPaymentResponse': xsd.Element(SendPaymentResponse()), 'GetRegistrationsFromSearchCriteria': xsd.Element(GetRegistrationsFromSearchCriteria()), 'GetRegistrationsFromSearchCriteriaResponse': xsd.Element(GetRegistrationsFromSearchCriteriaResponse()), 'GetRegistrationDetails': xsd.Element(GetRegistrationDetails()), 'GetRegistrationDetailsResponse': xsd.Element(GetRegistrationDetailsResponse()), 'SendRegistrationDetails': xsd.Element(SendRegistrationDetails()), 'SendRegistrationDetailsResponse': xsd.Element(SendRegistrationDetailsResponse())},
)