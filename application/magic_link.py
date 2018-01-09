'''
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Magic Link --

@author: Informed Solutions
'''


from .models import Login_And_Contact_Details, Application
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import EmailLogin, VerifyPhone
import json, random, requests, string, time, traceback



def existingApplicationView(request):
    
    # Initialise form
    form = EmailLogin()
    
    if request.method =='POST':
        
        form = EmailLogin(request.POST)
        
        # Retrieve e-mail address
        email = request.POST['email_address']
        
        # If a valid e-mail address has been submitted
        if form.is_valid():
            try:
                # Retrieve corresponding application
                acc = Login_And_Contact_Details.objects.get(email=email)
            except Exception as ex:
                return HttpResponseRedirect('/email-sent')
            #get url and substring just the domain
            domain = request.META.get('HTTP_REFERER', "")
            domain = domain[:-21]
            #generate random link
            
            link = generate_random(12, "link")
            #get current epoch so the link can be time-boxed
            expiry = int(time.time())
            #save link and expiry
            acc.email_expiry_date = expiry
            acc.magic_link_email=link
            acc.save()
            #send magic link email
            r = magic_link_email(email, domain +'validate/' +link)
            print(link)
            #Note that this is the same response whether the email is valid or not
            return HttpResponseRedirect('/email-sent') 
    
    return render(request, 'existing-application.html', {'form': form})
    
def magic_link_email(email, link_id):
    #Use Notify-Gateway API to send magic link email
    base_request_url = settings.NOTIFY_URL
    header = {'content-type': 'application/json'}
    input = {
        "email": email,
        "personalisation": {
        "link": link_id
    },
        "reference": "string",
        "templateId": "ecd2a788-257b-4bb9-8784-5aed82bcbb92"
    }
    r = requests.post(base_request_url + "/notify-gateway/api/v1/notifications/email/" , json.dumps(input), headers=header)
    return r
def magic_link_text(phone, link_id):
    #Use Notify-Gateway to send sms code
    base_request_url = settings.NOTIFY_URL
    header = {'content-type': 'application/json'}
    input = {
            "personalisation": {
            "link": link_id
        },
            "phoneNumber": phone,
            "reference": "string",
            "templateId": "d285f17b-8534-4110-ba6c-e7e788eeafb2"
            }
    r = requests.post(base_request_url + "/notify-gateway/api/v1/notifications/sms/" , json.dumps(input), headers=header)
    print(r.status_code)
    return(r)
def generate_random(digits, type):
    #generate a random code or random string of varying size depending on whether it's the SMS code or Magic Link url
    #digits is the length desired, and type can only be 'code' or 'link' anything else and it will break
    if(type == 'code'):
        r = ''.join([random.choice(string.digits) for n in range(digits)])
        #get expiry date
    elif(type == 'link'):
        r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(digits)])
        #get expiry date
    r = r.upper()
    return r


def hasExpired(expiry):
    #check to see whether a magic link url or sms code has expired
    #Expiry period is set in hours in the settings file
    exp_period=settings.EMAIL_EXPIRY*60*60
    #calculate difference between current time and when it was created
    diff = int(time.time()-expiry)
    
    if (diff <exp_period):
        #return false if it HAS NOT expired
        return False
    else:
        #Return true if it HAS expired
        return True

        
    
def validateMagicLink(request, id):
    #commented lines below check that the url matches the magic link (active lines check it vs phone number)
    try:
        acc = Login_And_Contact_Details.objects.get(magic_link_email=id)
        exp = acc.email_expiry_date
        if not hasExpired(exp) and len(id)>0:
            print('Success')
            #uncomment url if it should be a one-time use email
            #acc.magic_link_email = ""
            phone = acc.mobile_number
            g = generate_random(5, "code")
            expiry = int(time.time())
            acc.magic_link_sms = g
            acc.sms_expiry_date = expiry
            acc.save()
            magic_link_text(phone, g)
            #return JsonResponse({"message":"Link is valid, we just sent a text message to " +phone},status=200)
            return HttpResponseRedirect("/verifyPhone/?id="+id)
        else:
            return JsonResponse({"message":"The code has expired"},status=440)
    except Exception as ex:
        return JsonResponse({"message":"error bad link" + id}, status=404)
    
    return(JsonResponse({"message":"The id is: \'" +id +"\' | error link does not resolve"},status=400))


def SMSVerification(request):
    #This is the page where a user is redirected after clicking on their magic link
    #Unique form for entering SMS code (must be 5 digits in accordance with JIRA)
    form = VerifyPhone()
    id = request.GET['id']
    acc = Login_And_Contact_Details.objects.get(magic_link_email=id)
    login_id = acc.login_id
    application = Application.objects.get(login_id = login_id)
    
    #if request.method == 'GET':
    
        #print('Check')
    
    if request.method =='POST':
        print('Post')
        form = VerifyPhone(request.POST)
        code = request.POST['magic_link_sms']
        if len(code) == 0:
            exp = acc.email_expiry_date
            print(exp)
            print(id)
            print(hasExpired(exp))
            if not hasExpired(exp) and len(id)>0:
                print('Success')
                #uncomment url if it should be a one-time use email
                #acc.magic_link_email = ""
                phone = acc.mobile_number
                g = generate_random(5, "code")
                expiry = int(time.time())
                acc.magic_link_sms = g
                acc.sms_expiry_date = expiry
                acc.save()
                magic_link_text(phone, g)
                #return JsonResponse({"message":"Link is valid, we just sent a text message to " +phone},status=200)
                return HttpResponseRedirect("/verifyPhone/?id="+id)
        
        else:
            exp = acc.email_expiry_date
            if form.is_valid() and not hasExpired(exp):
                if code == acc.magic_link_sms:
                    #forward back onto appication
                    return HttpResponseRedirect("/task-list/?id="+str(application.application_id))
                else:
                    return(JsonResponse({"message":"FAILURE", "out":"code: " +str(code) +" | " +str(acc.magic_link_sms)},status=400))
        
    return render(request, 'verify-phone.html', {'form': form})