"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Worldpay Integration --

@author: Informed Solutions
"""

import json
import requests
from django.conf import settings


def make_payment(amount, name, number, cvc, expiry_m, expiry_y, currency, code, desc):
    """
    Function used to send a WorldPay card payment request to the payment gateway, all validation is done by the gateway,
    appropriate error response will be sent in JSON
    :param amount: amount of money to be charged, send as an integer. Done in pence, so £35 would be 3500
    :param name: name of the card holder, send as a string. This should be what is written on the card
    :param number: card number, sent as an integer. This should be what is written on the card
    :param cvc: cvc number on back of card. This should be sent as an integer
    :param expiry_m: expiry month on the card, sent as an integer. This should be what is written on the card
    :param expiry_y: expiry year on the card, sent as an integer. This should be what is written on the card
    :param currency: Currency code that should be charged, sent as a string, see below for full list:
    https://developer.worldpay.com/jsonapi/faq/articles/what-currencies-can-i-accept-payments-in
    :param code: This is the order code the customer will
    :param desc:
    :return:
    """
    base_url = settings.PAYMENT_URL

    header = {'content-type': 'application/json'}

    payload = {
        "amount": amount,
        "cardHolderName": name,
        "cardNumber": number,
        "cvc": cvc,
        "expiryMonth": expiry_m,
        "expiryYear": expiry_y,
        "currencyCode": currency,
        "customerOrderCode": code,
        "orderDescription": desc
    }

    response = requests.post(base_url + "/payment-gateway/api/v1/payments/card/", json.dumps(payload), headers=header)

    return response


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

    payload = {
        "email": email,
        "personalisation": {
            "firstName": name
        },
        "reference": "string",
        "templateId": "9c677777-95e0-424a-aaca-f9a4eec3c6b2"
    }

    response = requests.post(base_url + "/notify-gateway/api/v1/notifications/email/", json.dumps(payload),
                             headers=header)

    return response
