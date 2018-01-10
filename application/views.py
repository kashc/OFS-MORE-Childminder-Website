"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Views --

author: Informed Solutions
"""


import datetime
import json
import re
import time

from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import magic_link, payment, status
from .business_logic import (ChildcareType_Logic, dbs_check_logic, First_Aid_Logic, health_check_logic,
                             Login_Contact_Logic, Login_Contact_Logic_Phone, Multiple_Childcare_Address_Logic,
                             Personal_Childcare_Address_Logic, Personal_DOB_Logic, Personal_Home_Address_Logic,
                             Personal_Location_Of_Care_Logic, Personal_Name_Logic, references_check_logic)
from .forms import (ApplicationSaved, AccountForm, Confirm, ContactEmail, ContactPhone, ContactSummary,
                    DBSCheck, EmailLogin, Declaration, EYFS, FirstAidTrainingDetails,
                    FirstAidTrainingDeclaration, FirstAidTrainingGuidance, FirstAidTrainingTraining,
                    FirstAidTrainingRenew, FirstAidTrainingSummary, HealthDeclarationBooklet, OtherPeople,
                    Payment, PaymentDetails, PersonalDetailsChildcareAddress,
                    PersonalDetailsChildcareAddressManual, PersonalDetailsDOB, PersonalDetailsName,
                    PersonalDetailsGuidance, PersonalDetailsHomeAddress, PersonalDetailsHomeAddressManual,
                    PersonalDetailsLocationOfCare, PersonalDetailsSummary, Question,
                    ReferenceForm, TypeOfChildcare)
from .models import (Application, UserDetails, ApplicantPersonalDetails, ApplicantHomeAddress,
                     ApplicantName, First_Aid_Training)


# View for the start page
def StartPageView(request):

    # Create a blank user
    user = UserDetails.objects.create()

    # Create a new application
    application = Application.objects.create(
        application_type = 'CHILDMINDER',
        login_id = user,
        application_status = 'DRAFTING',
        cygnum_urn = '',
        login_details_status = 'NOT_STARTED',
        personal_details_status = 'NOT_STARTED',
        childcare_type_status = 'NOT_STARTED',
        first_aid_training_status = 'NOT_STARTED',
        eyfs_training_status = 'NOT_STARTED',
        criminal_record_check_status = 'NOT_STARTED',
        health_status = 'NOT_STARTED',
        references_status = 'NOT_STARTED',
        people_in_home_status = 'NOT_STARTED',
        declarations_status = 'NOT_STARTED',
        date_created = datetime.datetime.today(),
        date_updated = datetime.datetime.today(),
        date_accepted = None
    )

    # Access the task page
    return render(request, 'start-page.html', ({'id': application.application_id}))


# View for the account selection page
def AccountView(request):

    if request.method == 'GET':

        application_id = request.GET['id']

        form = AccountForm()

        # Access the task page
        return render(request, 'account-account.html', ({'application_id': application_id, 'form': form}))

    if request.method == 'POST':

        # Retrieve the application's ID
        application_id_local = request.POST["id"]

        form = AccountForm()

        # Return to the application's task list
        return HttpResponseRedirect('/account/email?id=' + application_id_local)

    else:

        variables = {
            'form': form,
            'application_id': application_id_local
        }

        # Return to the same page
        return render(request, 'account-account.html', variables)


# View for the task list
def LogInView(request):
           
    if request.method == 'GET':
        
        # Retrieve the application's ID
        application_id = request.GET["id"]
        
        # Retrieve application from database
        application = Application.objects.get(pk=application_id)
        
        # Generate a context for task statuses
        application_status_context = dict({
            'application_id': application_id,
            'login_details_status': application.login_details_status,
            'personal_details_status': application.personal_details_status,
            'childcare_type_status': application.childcare_type_status,
            'first_aid_training_status': application.first_aid_training_status,
            'eyfs_training_status': application.eyfs_training_status,
            'criminal_record_check_status': application.criminal_record_check_status,
            'health_status': application.health_status,
            'reference_status': application.references_status,
            'people_in_home_status': application.people_in_home_status,
            'declaration_status': application.declarations_status,
            'all_complete': False,
            'confirm_details': False
        })
        
        # Temporarily disable Declarations task if other tasks are still in progress
        temp_context = application_status_context
        del temp_context['declaration_status']
        
        if ('NOT_STARTED' in temp_context.values()) or ('IN_PROGRESS' in temp_context.values()):
            
            application_status_context['all_complete'] = False
            
        else:
            
            # Enable Declarations task when all other tasks are complete
            application_status_context['all_complete'] = True
            application_status_context['declaration_status'] = application.declarations_status
            
            # When the Declarations task is complete, enable button to confirm details
            if (application_status_context['declaration_status'] == 'COMPLETED'):
                
                application_status_context['confirm_details'] = True
            
            # Otherwise, disable the button to confirm details    
            else:
                
                application_status_context['confirm_details'] = False

    # Access the task page
    return render(request, 'task-list.html', application_status_context)


# View for the Type of childcare task
def TypeOfChildcareView(request):
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Type of childcare form
        form = TypeOfChildcare(request.POST, id = application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'
            status.update(application_id_local, 'childcare_type_status', 'COMPLETED')
            
            # Perform business logic to create or update Type of childcare record in database
            childcare_type_record = ChildcareType_Logic(application_id_local, form)
            childcare_type_record.save()
            
        # Return to the application's task list
        return HttpResponseRedirect('/task-list?id=' + application_id_local)
    
    # If the Type of childcare form is not completed    
    application_id_local = request.GET["id"]
    
    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).childcare_type_status != 'COMPLETED':
        
        status.update(application_id_local, 'childcare_type_status', 'IN_PROGRESS')
        
    form = TypeOfChildcare(id = application_id_local)
    
    # Access the task page
    return render(request, 'childcare.html', {'form': form, 'application_id': application_id_local})


# View for the Your login and contact details task: e-mail address
def ContactEmailView(request):
    
    # Get current date and time
    current_date = datetime.datetime.today()
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = ContactEmail(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'contact-email.html', {'form': form,'application_id': application_id_local, 'login_details_status': application.login_details_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = ContactEmail(request.POST,id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            email = form.cleaned_data['email_address']
            
            print(email)
            
            if UserDetails.objects.filter(email=email).exists():
            
                # Retrieve corresponding application
                acc = UserDetails.objects.get(email=email)
                #get url and substring just the domain
                domain = request.META.get('HTTP_REFERER', "")
                domain = domain[:-54]
                #generate random link
                
                link = magic_link.generate_random(12, "link")
                #get current epoch so the link can be time-boxed
                expiry = int(time.time())
                #save link and expiry
                acc.email_expiry_date = expiry
                acc.magic_link_email=link
                acc.save()
                #send magic link email
                r = magic_link.magic_link_email(email, domain +'validate/' +link)
                #Note that this is the same response whether the email is valid or not
                return HttpResponseRedirect('/email-sent?id=' + application_id_local)   
                
            else: 
            
                # Perform business logic to create or update Your login and contact details record in database
                login_and_contact_details_record = Login_Contact_Logic(application_id_local, form)
                login_and_contact_details_record.save()
                
                application.date_updated = current_date
                application.save()
        
                # Go to the phone numbers page   
                return HttpResponseRedirect('/account/phone?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'contact-email.html', {'form': form,'application_id': application_id_local})


# View for the Your login and contact details task: phone numbers
def ContactPhoneView(request):
    
    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = ContactPhone(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local) 
    
        # Access the task page
        return render(request, 'contact-phone.html', {'form': form,'application_id': application_id_local, 'login_details_status': application.login_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = ContactPhone(request.POST,id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Perform business logic to create or update Your login and contact details record in database
            login_and_contact_details_record = Login_Contact_Logic_Phone(application_id_local, form)
            login_and_contact_details_record.save()
            
            # Update application date updated
            application.date_updated = current_date
            application.save()
            
            # Return to the application's task list    
            return HttpResponseRedirect('/account/question?id=' + application_id_local)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'contact-phone.html', variables)


# View for the Your login and contact details task: knowledge-based question
def QuestionView(request):
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = Question(id = application_id_local)  
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)      
    
        # Access the task page
        return render(request, 'question.html', {'form': form,'application_id': application_id_local, 'login_details_status': application.login_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = Question(request.POST,id = application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Return to the application's task list    
            return HttpResponseRedirect('/account/summary?id=' + application_id_local)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'question.html', variables)
        

# View for the Your login and contact details task: phone numbers
def ContactSummaryView(request):
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        
        # Get associated user login ID
        login_id = Application.objects.get(pk=application_id_local).login_id.login_id
        
        # Retrieve answers
        email = UserDetails.objects.get(login_id=login_id).email
        mobile_number = UserDetails.objects.get(login_id=login_id).mobile_number
        add_phone_number = UserDetails.objects.get(login_id=login_id).add_phone_number
        
        # Update the status of the task to 'COMPLETED'
        if  Application.objects.get(pk = application_id_local).login_details_status != 'COMPLETED':
            
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
            
        form = ContactSummary()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)      
    
        # Access the task page
        return render(request, 'contact-summary.html', {'form': form,'application_id': application_id_local,'email': email,'mobile_number': mobile_number,'add_phone_number': add_phone_number, 'login_details_status': application.login_details_status, 'childcare_type_status': application.childcare_type_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = ContactSummary()
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
            
            # Return to the application's task list    
            return HttpResponseRedirect('/childcare?id=' + application_id_local)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'contact-summary.html', variables)


# View for the Your personal details task: guidance
def PersonalDetailsGuidanceView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = PersonalDetailsGuidance()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'personal-details-guidance.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = PersonalDetailsGuidance(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            
            # Go to the phone numbers page   
            return HttpResponseRedirect('/personal-details/name?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'personal-details-guidance.html', {'form': form,'application_id': application_id_local})


# View for the Your personal details task: names
def PersonalDetailsNameView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = PersonalDetailsName(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
    
        # Access the task page
        return render(request, 'personal-details-name.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = PersonalDetailsName(request.POST,id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            
            # Perform business logic to create or update Your personal details record in database
            applicant_names_record = Personal_Name_Logic(application_id_local, form)
            applicant_names_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            
            # Go to the date of birth page    
            return HttpResponseRedirect('/personal-details/dob/?id=' + application_id_local)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'personal-details-name.html', variables)


# View for the Your personal details task: date of birth
def PersonalDetailsDOBView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = PersonalDetailsDOB(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
    
        # Access the task page
        return render(request, 'personal-details-dob.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = PersonalDetailsDOB(request.POST,id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            
            # Perform business logic to create or update Your personal details record in database
            personal_details_record = Personal_DOB_Logic(application_id_local, form)
            personal_details_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            
            # Return to the application's task list    
            return HttpResponseRedirect('/personal-details/home-address?id=' + application_id_local + '&manual=False')
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'personal-details-dob.html', variables)
        

# View for the Your personal details task: home address
def PersonalDetailsHomeAddressView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        
        # If the user wants to use the postcode search
        if manual == 'False':    
            
            form = PersonalDetailsHomeAddress(id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
        
            # Access the task page
            return render(request, 'personal-details-home-address.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
        
        # If the user wants to manually enter their address
        elif manual == 'True':    
            
            form = PersonalDetailsHomeAddressManual(id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
        
            # Access the task page
            return render(request, 'personal-details-home-address-manual.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        
        # If the user wants to use the postcode search        
        if manual == 'False':
        
            # Initialise the Your login and contact details form
            form = PersonalDetailsHomeAddress(request.POST,id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
            
            # If the form is successfully submitted (with valid details)
            if form.is_valid():
                
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/home-address/?id=' + application_id_local + '&manual=False')
            
            else: 
            
                # Access the task page
                return render(request, 'personal-details-home-address.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
        
        # If the user wants to manually enter their address    
        if manual == 'True':
        
            # Initialise the Your login and contact details form
            form = PersonalDetailsHomeAddressManual(request.POST,id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
            
            # If the form is successfully submitted (with valid details)
            if form.is_valid():
                
                # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
                if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                
                # Perform business logic to create or update Your personal details record in database
                home_address_record = Personal_Home_Address_Logic(application_id_local, form)
                home_address_record.save()
    
                # Update application date updated
                application = Application.objects.get(pk=application_id_local)
                application.date_updated = current_date
                application.save()
                
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/location-of-care?id=' + application_id_local)
            
            else: 
            
                # Access the task page
                return render(request, 'personal-details-home-address-manual.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})   


# View for the Your personal details task: location of care
def PersonalDetailsLocationOfCareView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
       
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        
        # Get associated personal detail ID
        personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=application_id_local).personal_detail_id
        
        Multiple_Childcare_Address_Logic(personal_detail_id)
        
        # Retrieve answers
        street_line1 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).street_line1
        street_line2 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).street_line2
        town = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).town
        county = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).county
        postcode = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).postcode
        
        # Update the status of the task to 'COMPLETED'
        if  Application.objects.get(pk = application_id_local).login_details_status != 'COMPLETED':
            
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
            
        form = PersonalDetailsLocationOfCare(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)      
    
        # Access the task page
        return render(request, 'personal-details-location-of-care.html', {'form': form,'application_id': application_id_local,'street_line1': street_line1,'street_line2': street_line2,'town': town, 'county': county, 'postcode': postcode, 'personal_details_status': application.login_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]

        # Get associated personal detail ID
        personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=application_id_local).personal_detail_id
        
        # Initialise the Your login and contact details form
        form = PersonalDetailsLocationOfCare(request.POST,id = application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            
            # Perform business logic to create or update Your personal details record in database
            home_address_record = Personal_Location_Of_Care_Logic(application_id_local, form)
            home_address_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()

            Multiple_Childcare_Address_Logic(personal_detail_id)
            
            if home_address_record.childcare_address == 'True':
            
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/summary?id=' + application_id_local)
            
            elif home_address_record.childcare_address == 'False':
                
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/childcare-address?id=' + application_id_local + '&manual=False')
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'personal-details-location-of-care.html', variables)       


# View for the Your personal details task: childcare address
def PersonalDetailsChildcareAddressView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        
        # If the user wants to use the postcode search
        if manual == 'False':  
            
            form = PersonalDetailsChildcareAddress(id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
        
            # Access the task page
            return render(request, 'personal-details-childcare-address.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
        
        # If the user wants to manually enter their address
        elif manual == 'True':    
            
            form = PersonalDetailsChildcareAddressManual(id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
        
            # Access the task page
            return render(request, 'personal-details-childcare-address-manual.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        
        # If the user wants to use the postcode search        
        if manual == 'False':
        
            # Initialise the Your login and contact details form
            form = PersonalDetailsChildcareAddress(request.POST,id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
            
            # If the form is successfully submitted (with valid details)
            if form.is_valid():

                # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
                if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/childcare-address/?id=' + application_id_local + '&manual=False')
            
            else: 
            
                # Access the task page
                return render(request, 'personal-details-childcare-address.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status})
        
        # If the user wants to manually enter their address    
        if manual == 'True':
        
            # Initialise the Your login and contact details form
            form = PersonalDetailsChildcareAddressManual(request.POST,id = application_id_local)
            
            # Retrieve application from database for Back button/Return to list link logic
            application = Application.objects.get(pk=application_id_local)
            
            # If the form is successfully submitted (with valid details)
            if form.is_valid():
                
                # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
                if  Application.objects.get(pk = application_id_local).personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                
                # Perform business logic to create or update Your personal details record in database
                childcare_address_record = Personal_Childcare_Address_Logic(application_id_local, form)
                childcare_address_record.save()
    
                # Update application date updated
                application = Application.objects.get(pk=application_id_local)
                application.date_updated = current_date
                application.save()
                
                # Return to the application's task list    
                return HttpResponseRedirect('/personal-details/summary?id=' + application_id_local)
            
            else: 
            
                # Access the task page
                return render(request, 'personal-details-childcare-address-manual.html', {'form': form,'application_id': application_id_local, 'personal_details_status': application.personal_details_status}) 


# View for the Your personal details task: summary
def PersonalDetailsSummaryView(request):
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        
        # Get associated personal detail ID
        personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=application_id_local)
        
        # Retrieve answers
        birth_day = personal_detail_id.birth_day
        birth_month = personal_detail_id.birth_month
        birth_year = personal_detail_id.birth_year
        first_name = ApplicantName.objects.get(personal_detail_id=personal_detail_id).first_name
        middle_names = ApplicantName.objects.get(personal_detail_id=personal_detail_id).middle_names
        last_name = ApplicantName.objects.get(personal_detail_id=personal_detail_id).last_name
        street_line1 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).street_line1
        street_line2 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).street_line2
        town = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).town
        county = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).county
        postcode = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).postcode
        location_of_childcare = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, current_address=True).childcare_address
        childcare_street_line1 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, childcare_address=True).street_line1
        childcare_street_line2 = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, childcare_address=True).street_line2
        childcare_town = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, childcare_address=True).town
        childcare_county = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, childcare_address=True).county
        childcare_postcode = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id, childcare_address=True).postcode
            
        form = PersonalDetailsSummary()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Update the status of the task to 'COMPLETED'
        status.update(application_id_local, 'personal_details_status', 'COMPLETED')      
    
        # Access the task page
        return render(request, 'personal-details-summary.html', {'form': form,'application_id': application_id_local,'first_name': first_name,'middle_names': middle_names,'last_name': last_name, 'birth_day': birth_day, 'birth_month': birth_month, 'birth_year': birth_year, 'street_line1': street_line1, 'street_line2': street_line2, 'town': town, 'county': county, 'postcode': postcode, 'location_of_childcare': location_of_childcare, 'childcare_street_line1': childcare_street_line1, 'childcare_street_line2': childcare_street_line2, 'childcare_town': childcare_town, 'childcare_county': childcare_county, 'childcare_postcode': childcare_postcode, 'personal_details_status': application.personal_details_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = PersonalDetailsSummary()
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'
            status.update(application_id_local, 'personal_details_status', 'COMPLETED')
            
            # Return to the application's task list    
            return HttpResponseRedirect('/task-list?id=' + application_id_local)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'personal-details-summary.html', variables)


# View for the First aid training task: guidance
def FirstAidTrainingGuidanceView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = FirstAidTrainingGuidance()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'first-aid-guidance.html', {'form': form,'application_id': application_id_local, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingGuidance(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).first_aid_training_status != 'COMPLETED':
                status.update(application_id_local, 'first_aid_training_status', 'IN_PROGRESS')
            
            # Go to the details page   
            return HttpResponseRedirect('/first-aid/details?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'first-aid-training-guidance.html', {'form': form,'application_id': application_id_local})                     


# View for the First aid training: details
def FirstAidTrainingDetailsView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'GET':
        
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = FirstAidTrainingDetails(id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
    
        # Access the task page
        return render(request, 'first-aid-details.html', {'form': form,'application_id': application_id_local, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingDetails(request.POST,id = application_id_local)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed    
            if  Application.objects.get(pk = application_id_local).first_aid_training_status != 'COMPLETED':
                status.update(application_id_local, 'first_aid_training_status', 'IN_PROGRESS')
            
            # Perform business logic to create or update First aid training record in database
            first_aid_training_record = First_Aid_Logic(application_id_local, form)
            first_aid_training_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            
            # Verify if first aid training certificate needs to be renewed
            # Get certificate date
            certificate_day = form.cleaned_data['course_date'].day
            certificate_month = form.cleaned_data['course_date'].month
            certificate_year = form.cleaned_data['course_date'].year
            certificate_date = date(certificate_year, certificate_month, certificate_day)
            
            # Get today's date
            today = date.today()
            
            # Calculate certificate age
            certificate_age = today.year - certificate_date.year - ((today.month, today.day) < (certificate_date.month, certificate_date.day))
        
            # If the certificate is less than 2.5 years old
            if (certificate_age < 2.5):
            
                # Go to the declaration page    
                return HttpResponseRedirect('/first-aid/declaration?id=' + application_id_local)
            
            # If the certificate is between 2.5 and 3 years old
            elif (2.5 <= certificate_age <= 3):
                
                # Go to the renew page    
                return HttpResponseRedirect('/first-aid/renew?id=' + application_id_local)
            
            # If the certificate is older than 3 years
            elif (certificate_age > 3):
                
                # Go to the renew page    
                return HttpResponseRedirect('/first-aid/training?id=' + application_id_local)                               
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'first-aid-details.html', variables)


# View for the First aid training task: declaration
def FirstAidTrainingDeclarationView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = FirstAidTrainingDeclaration()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'first-aid-declaration.html', {'form': form,'application_id': application_id_local, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingDeclaration(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            status.update(application_id_local, 'first_aid_training_status', 'COMPLETED')
            
            # Go to the details page   
            return HttpResponseRedirect('/first-aid/summary?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'first-aid-declaration.html', {'form': form,'application_id': application_id_local}) 


# View for the First aid training task: renew
def FirstAidTrainingRenewView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = FirstAidTrainingRenew()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'first-aid-renew.html', {'form': form,'application_id': application_id_local, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingRenew(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            status.update(application_id_local, 'first_aid_training_status', 'COMPLETED')
            
            # Go to the details page   
            return HttpResponseRedirect('/first-aid/summary?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'first-aid-renew.html', {'form': form,'application_id': application_id_local}) 


# View for the First aid training task: training
def FirstAidTrainingTrainingView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
            
        form = FirstAidTrainingTraining()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'first-aid-training.html', {'form': form,'application_id': application_id_local, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingTraining(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'NOT_STARTED'    
            status.update(application_id_local, 'first_aid_training_status', 'NOT_STARTED')
            
            # Go to the details page   
            return HttpResponseRedirect('/first-aid/summary?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'first-aid-training.html', {'form': form,'application_id': application_id_local}) 
        
        
# View for the First aid training task: summary
def FirstAidTrainingSummaryView(request):
        
    if request.method =='GET':
          
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        
        # Retrieve answers
        training_organisation = First_Aid_Training.objects.get(application_id=application_id_local).training_organisation
        training_course = First_Aid_Training.objects.get(application_id=application_id_local).course_title
        certificate_day = First_Aid_Training.objects.get(application_id=application_id_local).course_day
        certificate_month = First_Aid_Training.objects.get(application_id=application_id_local).course_month
        certificate_year = First_Aid_Training.objects.get(application_id=application_id_local).course_year
            
        form = FirstAidTrainingSummary()
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # Access the task page
        return render(request, 'first-aid-summary.html', {'form': form,'application_id': application_id_local, 'training_organisation': training_organisation, 'training_course': training_course, 'certificate_day': certificate_day, 'certificate_month': certificate_month, 'certificate_year': certificate_year, 'first_aid_training_status': application.first_aid_training_status})
    
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your login and contact details form
        form = FirstAidTrainingSummary(request.POST)
        
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Go to the details page   
            return HttpResponseRedirect('/task-list?id=' + application_id_local)
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'first-aid-summary.html', {'form': form,'application_id': application_id_local}) 


# View for the Early Years knowledge task
def EYFSView(request):
   
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Early Years knowledge form
        form = EYFS(request.POST)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'
            status.update(application_id_local, 'eyfs_training_status', 'COMPLETED')
            
        # Return to the application's task list    
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the Early Years knowledge form is not completed
    application_id_local = request.GET["id"]

    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).eyfs_training_status != 'COMPLETED':
        
        status.update(application_id_local, 'eyfs_training_status', 'IN_PROGRESS')
    
    form = EYFS()
    
    # Access the task page
    return render(request, 'eyfs.html', {'application_id': application_id_local})


# View for the Your criminal record (DBS) check task
def DBSCheckView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
   
    if request.method =='POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your criminal record (DBS) check form
        form = DBSCheck(request.POST, id = application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'
            status.update(application_id_local, 'criminal_record_check_status', 'COMPLETED')
            
            # Perform business logic to create or update Your criminal record (DBS) check record in database
            dbs_check_record = dbs_check_logic(application_id_local, form)
            dbs_check_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            
        # Return to the application's task list
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the Your criminal record (DBS) check form is not completed
    application_id_local = request.GET["id"]
    
    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).criminal_record_check_status != 'COMPLETED':
        
        status.update(application_id_local, 'criminal_record_check_status', 'IN_PROGRESS')
    
    form = DBSCheck(id = application_id_local)
    
    # Access the task page
    return render(request, 'dbs-check.html', {'form': form,'application_id': application_id_local})


# View for the Your health task
def HealthView(request):
    
    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Your health form
        form = HealthDeclarationBooklet(request.POST, id = application_id_local)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'            
            status.update(application_id_local, 'health_status', 'COMPLETED')
            
            # Perform business logic to create or update Your health record in database            
            health_record = health_check_logic(application_id_local, form)
            health_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            
        # Return to the application's task list
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the Your health form is not completed    
    application_id_local = request.GET["id"]
    
    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).health_status != 'COMPLETED':
        
        status.update(application_id_local, 'health_status', 'IN_PROGRESS')
    
    form = HealthDeclarationBooklet(id = application_id_local)
    
    # Access the task page
    return render(request, 'health.html', {'form': form,'application_id': application_id_local})


# View for the 2 references task
def ReferencesView(request):

    # Get current date and time
    current_date = datetime.datetime.today()
    
    if request.method == 'POST':
        
        # Retrieve the application's ID        
        application_id_local = request.POST["id"]
        
        # Initialise the 2 references form
        form = ReferenceForm(request.POST,id = application_id_local)
        
        # If the form is successfully submitted (with valid details) 
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'              
            status.update(application_id_local, 'references_status', 'COMPLETED')

            # Perform business logic to create or update 2 references record in database              
            references_record = references_check_logic(application_id_local, form)
            references_record.save()

            # Update application date updated
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()

        # Return to the application's task list            
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the 2 references form is not completed 
    application_id_local = request.GET["id"]

    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).references_status != 'COMPLETED':
        
        status.update(application_id_local, 'references_status', 'IN_PROGRESS')
    
    form = ReferenceForm(id = application_id_local)
    
    # Access the task page
    return render(request, 'references.html', {'form': form,'application_id': application_id_local})  


# View for the People in your home task
def OtherPeopleView(request):
    
    if request.method == 'POST':
        
        # Retrieve the application's ID         
        application_id_local = request.POST["id"]
        
        # Initialise the People in your home form        
        form = OtherPeople(request.POST)
        
        # If the form is successfully submitted (with valid details)         
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED' 
            status.update(application_id_local, 'people_in_home_status', 'COMPLETED')
        
        # Return to the application's task list              
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the People in your home form is not completed 
    application_id_local = request.GET["id"]
    
    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).people_in_home_status != 'COMPLETED':
        
        status.update(application_id_local, 'people_in_home_status', 'IN_PROGRESS')
    
    form = OtherPeople()
    
    # Access the task page
    return render(request, 'other-people.html', {'application_id': application_id_local}) 


# View for the Declaration task
def DeclarationView(request):

    if request.method == 'POST':
        
        # Retrieve the application's ID         
        application_id_local = request.POST["id"]
        
        # Initialise the Declaration form
        form = Declaration(request.POST)
        
        # If the form is successfully submitted (with valid details) 
        if form.is_valid():
            
            # Update the status of the task to 'COMPLETED'            
            status.update(application_id_local, 'declarations_status', 'COMPLETED')
            
        # Return to the application's task list         
        return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    # If the People in your home form is not completed    
    application_id_local = request.GET["id"]
    
    # Update the status of the task to 'IN_PROGRESS' if the task has not yet been completed
    if  Application.objects.get(pk = application_id_local).declarations_status != 'COMPLETED':
    
        status.update(application_id_local, 'declarations_status', 'COMPLETED')
    
    form = Declaration()
    
    # Access the task page
    return render(request, 'declaration.html', {'application_id': application_id_local})


# View for the Confirm your details page
def ConfirmationView(request):
    
    if request.method == 'POST':
        
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        
        # Initialise the Confirm your details form        
        form = Confirm(request.POST)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Return to the application's task list 
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)

    # If the Confirm your details form is not completed     
    application_id_local = request.GET["id"]
    form = Confirm()
    
    # Access the page
    return render(request, 'confirm.html', {'application_id': application_id_local})


# View the Payment page
def PaymentView(request):
    
    if request.method == 'GET':
        
        #Get the application
        application_id_local = request.GET["id"]

        # As not data is saved for this, a blank payment form is generated with each get request       
        form = Payment()
    
        # Access the task page
        return render(request, 'payment.html', {'form': form,'application_id': application_id_local})        
    
    if request.method == 'POST':
        
        # Retrieve the application's ID        
        application_id_local = request.POST["id"]
        
        # Initialise the Payment form        
        form = Payment(request.POST)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Get selected payment method
            payment_method = form.cleaned_data['payment_method']
            
            if (payment_method == 'Credit'):
            
                # Navigate to the payment details page
                return HttpResponseRedirect('/payment-details/?id=' + application_id_local)
            
            elif (payment_method == 'PayPal'):
                
                # Stay on the same page
                return HttpResponseRedirect('https://www.paypal.com/uk/home')
        
        # If there are invalid details
        else:
            
            # Return to the same page
            return render(request, 'payment.html', {'form': form, 'application_id': application_id_local})


# View the Payment Details page
def CardPaymentDetailsView(request):
    
    if request.method == 'GET':
        
        #Get the application
        application_id_local = request.GET["id"]

        # As no data is saved for this, a blank payment form is generated with each get request       
        form = PaymentDetails()
    
        # Access the task page
        return render(request, 'payment-details.html', {'form': form,'application_id': application_id_local})
    
    if request.method == 'POST':
        
        #Get the application
        application_id_local = request.POST["id"]
               
        # Initialise the Payment Details form
        form = PaymentDetails(request.POST)
        
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            
            # Retrieve data
            card_number = re.sub('[ -]+', '', request.POST["card_number"]) 
            cardholders_name = request.POST["cardholders_name"]
            card_security_code = request.POST["card_security_code"]
            expiry_month = request.POST["expiry_date_0"]
            expiry_year = request.POST["expiry_date_1"]
            
            # Make payment
            payment_response = payment.make_payment(3500, cardholders_name, card_number, card_security_code, expiry_month, expiry_year, 'GBP', application_id_local, 'Childminder registration fee')
            # Parse payment response
            parsed_payment_response = json.loads(payment_response.text)
            
            # If the payment is successful
            if payment_response.status_code == 201:
                application = Application.objects.get(pk=application_id_local)
                login_id = application.login_id.login_id
                login_record = UserDetails.objects.get(pk=login_id)
                personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=application_id_local).personal_detail_id
                applicant_name_record = ApplicantName.objects.get(personal_detail_id=personal_detail_id)
                email_response = payment.payment_email(login_record.email, applicant_name_record.first_name)
                
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'order_code': parsed_payment_response["orderCode"],
                }
                
                # Go to payment confirmation page                         
                return render(request, 'payment-confirmation.html', variables)
           
            else:
                
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'error_flag': 1,
                    'error_message': parsed_payment_response["message"],
                }
            
            # Return to the application's task list    
            return HttpResponseRedirect(request, '/payment-details/?id=' + application_id_local, variables)
    
        # If there are invalid details
        else:
            
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            
            # Return to the same page
            return render(request, 'payment-details.html', variables)


# View the Application saved page
def ApplicationSavedView(request):
    
    if request.method == 'POST':
        
        # Retrieve the application's ID         
        application_id_local = request.POST["id"]
        
        # Initialise the Application saved form        
        form = ApplicationSaved(request.POST)
        
        # If the form is successfully submitted (with valid details)        
        if form.is_valid():
            
            # Stay on the same page
            return HttpResponseRedirect('/application-saved/?id=' + application_id_local)
    
    # If the Application saved form is not completed
    application_id_local = request.GET["id"]
    form = ApplicationSaved()
    
    # Access the page
    return render(request, 'application-saved.html', {'form': form, 'application_id': application_id_local})


# Reset view, to set all tasks to To Do
def ResetView(request):
    
    # Create a list of task statuses
    SECTION_LIST = ['login_details_status', 'personal_details_status', 'childcare_type_status', 'first_aid_training_status', 'eyfs_training_status', 'criminal_record_check_status', 'health_status', 'references_status', 'people_in_home_status', 'declarations_status']    
    
    # Retrieve the application's ID     
    application_id_local = request.GET["id"]
    
    # For each task in the list of task statuses
    for section in SECTION_LIST:
        
        # Set the progress status to To Do
        status.update(application_id_local, section, 'NOT_STARTED')
     
    # Access the task list   
    return HttpResponseRedirect('/task-list/?id=' + application_id_local)





#Test View, will change
def existingApplicationView(request):
    form = EmailLogin()
    if request.method =='POST':
        print (request)
    return render(request, 'existing-application.html', {'form': form})