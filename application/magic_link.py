import requests
import json
import random, string

def start(self):
    g = generate_random_link(7)
    #sendEmail = magic_link_email("matthew.styles@informed.com",g)
    g = generate_random_link(4)
    sendSMS = magic_link_sms("07557986930",g)
def magic_link_email(email, link_id):
    base_request_url='http://130.130.52.132:8095'
    header = {'content-type': 'application/json'}
    input = {
        "email": email,
        "personalisation": {
        "link": '/validate/' +link_id
    },
        "reference": "string",
        "templateId": "ecd2a788-257b-4bb9-8784-5aed82bcbb92"
    }
    r = requests.post(base_request_url + "/notify-gateway/api/v1/notifications/email/" , json.dumps(input), headers=header)
    print(r.status_code)
    return(r)
def magic_link_sms(phone, link_id):
    base_request_url='http://130.130.52.132:8095'
    header = {'content-type': 'application/json'}
    input = {
            "personalisation": {
            "link": '/validate/' +link_id
        },
            "phoneNumber": phone,
            "reference": "string",
            "templateId": "d285f17b-8534-4110-ba6c-e7e788eeafb2"
            }
    r = requests.post(base_request_url + "/notify-gateway/api/v1/notifications/sms/" , json.dumps(input), headers=header)
    print(r.status_code)
    return(r)
def generate_random_link(digits):
    #input the length and it will generate a random set of numbers (or both if you use the line below)
    is_set = False
    while(is_set == False):
        r = ''.join([random.choice(string.digits) for n in range(digits)])
        #this line outputs random letters and digits
        #r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(digits)])
        r = r.upper()
        #Add if statement, if this link exists (check SMS and email) generate again
        if is_set:
            break
        else:
            is_set = True
    return r
def lookup_magic_link(link_id):
    #add code to lookup the link id, check that it's within expiry date, and return email address if successful
    return