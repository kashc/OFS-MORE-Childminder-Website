import requests
import json
from django.conf import settings


def make_payment(amount, name, number, cvc, expiryM, expiryY, currency, code, desc):
    
    base_url = settings.PAYMENT_URL
    
    header = {'content-type': 'application/json'}
    
    input = {
        "amount": amount,
        "cardHolderName": name,
        "cardNumber": number,
        "cvc": cvc,
        "expiryMonth": expiryM,
        "expiryYear": expiryY,
        "currencyCode": currency,
        "customerOrderCode": code,
        "orderDescription": desc
    }
    
    r = requests.post(base_url + "/payment-gateway/api/v1/payments/card/" , json.dumps(input), headers=header)   
    
    return r

def payment_email(email, name):

    base_url = settings.NOTIFY_URL

    header = {'content-type': 'application/json'}
    
    input = {
        "email": email,
        "personalisation": {
            "firstName" : name
        },
        "reference": "string",
        "templateId": "9c677777-95e0-424a-aaca-f9a4eec3c6b2"
    }
    
    r = requests.post(base_url + "/notify-gateway/api/v1/notifications/email/" , json.dumps(input), headers=header)
    print("Payment Email Sent")
    return(r)