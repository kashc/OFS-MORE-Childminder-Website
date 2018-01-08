import requests
import json

def start(self):
    
    p = make_payment(10, "matt", 5454545454545454, 111, 4, 2019, "GBP", "OFS-MORE-162738", "Registration Fee")
    
    if(p.status_code==200):
        
        send = payment_email("matthew.styles@informed.com", "Matt")
    
def make_payment(amount, name, number, cvc, expiryM, expiryY, currency, code, desc):
    
    base_url = 'http://130.130.52.132:8089'
    
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
    
    base_url='http://130.130.52.132:8095'
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
    
    return(r)