"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Worldpay Integration --

@author: Informed Solutions
"""

import json
import requests
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

    r = requests.post(base_url + "/payment-gateway/api/v1/payments/card/", json.dumps(input), headers=header)

    return r


def make_paypal_payment(shopper_country_code, amount, currency_code, order_description, customer_order_code,
                        success_url, pending_url, failure_url, cancel_url):
    base_url = settings.PAYMENT_URL

    header = {'content-type': 'application/json'}

    payload = {
        "shopperCountryCode": shopper_country_code,
        "amount": amount,
        "currencyCode": currency_code,
        "customerOrderCode": customer_order_code,
        "orderDescription": order_description,
        "successUrl": success_url,
        "pendingUrl": pending_url,
        "failureUrl": failure_url,
        "cancellationUrl": cancel_url,
    }

    response = requests.post(base_url + "/payment-gateway/api/v1/payments/paypal/", json.dumps(payload), headers=header)

    # We deal with the entire object as parsing out just the requestURL in the payment API may be undesirbale for other
    # services
    response_url = json.loads(response.text)["redirectURL"]

    return response_url

def check_payment(order_code):
    base_url = settings.PAYMENT_URL
    header = {'content-type': 'application/json'}
    response = requests.get(base_url + "/payment-gateway/api/v1/payments/" + order_code, headers=header)

    return response.status_code


def payment_email(email, name):
    base_url = settings.NOTIFY_URL

    header = {'content-type': 'application/json'}

    input = {
        "email": email,
        "personalisation": {
            "firstName": name
        },
        "reference": "string",
        "templateId": "9c677777-95e0-424a-aaca-f9a4eec3c6b2"
    }

    r = requests.post(base_url + "/notify-gateway/api/v1/notifications/email/", json.dumps(input), headers=header)
    print("Payment Email Sent")
    return (r)
