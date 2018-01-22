"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- views.py --

@author: Informed Solutions
"""

import datetime
import json
import re
import time
from datetime import date
from uuid import UUID

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from . import magic_link, payment, status
from .business_logic import (childcare_type_logic,
                             dbs_check_logic,
                             first_aid_logic,
                             health_check_logic,
                             login_contact_logic,
                             login_contact_logic_phone,
                             multiple_childcare_address_logic,
                             personal_childcare_address_logic,
                             personal_dob_logic,
                             personal_home_address_logic,
                             personal_location_of_care_logic,
                             personal_name_logic,
                             references_first_reference_logic,
                             references_second_reference_logic)
from .forms import (AccountForm, ApplicationSavedForm, ConfirmForm, ContactEmailForm, ContactPhoneForm,
                    ContactSummaryForm, DBSCheckDBSDetailsForm, DBSCheckGuidanceForm, DBSCheckSummaryForm,
                    DBSCheckUploadDBSForm, DeclarationForm, EYFSForm, FirstAidTrainingDeclarationForm,
                    FirstAidTrainingDetailsForm, FirstAidTrainingGuidanceForm, FirstAidTrainingRenewForm,
                    FirstAidTrainingSummaryForm, FirstAidTrainingTrainingForm, FirstReferenceForm, HealthBookletForm,
                    HealthIntroForm, OtherPeopleForm, PaymentDetailsForm, PaymentForm,
                    PersonalDetailsChildcareAddressForm, PersonalDetailsChildcareAddressManualForm,
                    PersonalDetailsDOBForm, PersonalDetailsGuidanceForm, PersonalDetailsHomeAddressForm,
                    PersonalDetailsHomeAddressManualForm, PersonalDetailsLocationOfCareForm, PersonalDetailsNameForm,
                    PersonalDetailsSummaryForm, QuestionForm, ReferenceFirstReferenceAddressForm,
                    ReferenceFirstReferenceAddressManualForm, ReferenceFirstReferenceContactForm, ReferenceIntroForm,
                    ReferenceSecondReferenceAddressForm, ReferenceSecondReferenceAddressManualForm,
                    ReferenceSecondReferenceContactForm, ReferenceSummaryForm, SecondReferenceForm, TypeOfChildcareForm)
from .middleware import CustomAuthenticationHandler
from .models import (ApplicantHomeAddress, ApplicantName, ApplicantPersonalDetails, Application, CriminalRecordCheck,
                     FirstAidTraining, HealthDeclarationBooklet, Reference, UserDetails)


def error_404(request):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)


def start_page(request):
    """
    Method returning the template for the start page
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered start page template
    """
    return render(request, 'start-page.html')


def account_selection(request):
    """
    Method returning the template for the account selection page and navigating to the account: email page when
    clicking on the Create an account button, which triggers the creation of a new application
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered account selection template
    """
    if request.method == 'GET':
        form = AccountForm()
        variables = {
            'form': form,
        }
        return render(request, 'account-account.html', variables)
    if request.method == 'POST':
        user = UserDetails.objects.create()
        application = Application.objects.create(
            application_type='CHILDMINDER',
            login_id=user,
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='NOT_STARTED',
            personal_details_status='NOT_STARTED',
            childcare_type_status='NOT_STARTED',
            first_aid_training_status='NOT_STARTED',
            eyfs_training_status='NOT_STARTED',
            criminal_record_check_status='NOT_STARTED',
            health_status='NOT_STARTED',
            references_status='NOT_STARTED',
            people_in_home_status='NOT_STARTED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None,
            order_code=None
        )
        application_id_local = str(application.application_id)
        return HttpResponseRedirect(settings.URL_PREFIX + '/account/email?id=' + application_id_local)
    else:
        form = AccountForm()
        variables = {
            'form': form
        }
        return render(request, 'account-account.html', variables)


def contact_email(request):
    """
    Method returning the template for the Your login and contact details: email page (for a given application)
    and navigating to the Your login and contact details: phone number page when successfully completed;
    business logic is applied to either create or update the associated User_Details record; the page redirects
    the applicant to the login page if they have previously applied
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your login and contact details: email template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ContactEmailForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'login_details_status': application.login_details_status
        }
        return render(request, 'contact-email.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ContactEmailForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            # Send login e-mail link if applicant has previously applied
            email = form.cleaned_data['email_address']
            if UserDetails.objects.filter(email=email).exists():
                acc = UserDetails.objects.get(email=email)
                domain = request.META.get('HTTP_REFERER', "")
                domain = domain[:-54]
                link = magic_link.generate_random(12, "link")
                expiry = int(time.time())
                acc.email_expiry_date = expiry
                acc.magic_link_email = link
                acc.save()
                magic_link.magic_link_email(email, domain + 'validate/' + link)
                return HttpResponseRedirect(settings.URL_PREFIX + '/email-sent?id=' + application_id_local)
            else:
                # Create or update User_Details record
                user_details_record = login_contact_logic(application_id_local, form)
                user_details_record.save()
                application.date_updated = current_date
                application.save()
                response = HttpResponseRedirect(settings.URL_PREFIX + '/account/phone?id=' + application_id_local)
                # Create session and issue cookie to user
                CustomAuthenticationHandler.create_session(response, application.login_id.email)
                return response
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': application.login_details_status
            }
            return render(request, 'contact-email.html', variables)


def contact_phone(request):
    """
    Method returning the template for the Your login and contact details: phone number page (for a given application)
    and navigating to the Your login and contact details: question page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your login and contact details: phone template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ContactPhoneForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'login_details_status': application.login_details_status
        }
        return render(request, 'contact-phone.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ContactPhoneForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            # Update User_Details record
            user_details_record = login_contact_logic_phone(application_id_local, form)
            user_details_record.save()
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/account/question?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': application.login_details_status
            }
            return render(request, 'contact-phone.html', variables)


def contact_question(request):
    """
    Method returning the template for the Your login and contact details: question page (for a given application)
    and navigating to the Your login and contact details: summary page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your login and contact details: question template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = QuestionForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'login_details_status': application.login_details_status
        }
        return render(request, 'contact-question.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = QuestionForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        # If form is not empty
        if form.is_valid():
            # Save security question and answer
            login_id = application.login_id.login_id
            acc = UserDetails.objects.get(login_id=login_id)
            security_answer = form.clean_security_answer()
            security_question = form.clean_security_question()
            acc.security_question = security_question
            acc.security_answer = security_answer
            acc.save()

            return HttpResponseRedirect(settings.URL_PREFIX + '/account/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': application.login_details_status
            }
            return render(request, 'contact-question.html', variables)


def contact_summary(request):
    """
    Method returning the template for the Your login and contact details: summary page (for a given application)
    displaying entered data for this task and navigating to the Type of childcare page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your login and contact details: summary template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        application = Application.objects.get(pk=application_id_local)
        login_id = application.login_id.login_id
        user_details = UserDetails.objects.get(login_id=login_id)
        email = user_details.email
        mobile_number = user_details.mobile_number
        add_phone_number = user_details.add_phone_number
        if application.login_details_status != 'COMPLETED':
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
        form = ContactSummaryForm()
        variables = {
            'form': form,
            'application_id': application_id_local,
            'email': email,
            'mobile_number': mobile_number,
            'add_phone_number': add_phone_number,
            'login_details_status': application.login_details_status,
            'childcare_type_status': application.childcare_type_status
        }
        return render(request, 'contact-summary.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ContactSummaryForm()
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/childcare?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': application.login_details_status
            }
            return render(request, 'contact-summary.html', variables)


def type_of_childcare(request):
    """
    Method returning the template for the Type of childcare page (for a given application) and navigating to
    the task list when successfully completed; business logic is applied to either create or update the
    associated Childcare_Type record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Type of childcare template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = TypeOfChildcareForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'childcare_type_status': application.childcare_type_status
        }
        return render(request, 'childcare.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = TypeOfChildcareForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            # Create or update Childcare_Type record
            childcare_type_record = childcare_type_logic(application_id_local, form)
            childcare_type_record.save()
            application.date_updated = current_date
            application.save()
            status.update(application_id_local, 'childcare_type_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'childcare_type_status': application.childcare_type_status
            }
            return render(request, 'childcare.html', variables)


def task_list(request):
    """
    Method returning the template for the task-list (with current task status) for an applicant's application;
    logic is built in to enable the Declarations and Confirm your details tasks when all other tasks are complete
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered task list template
    """
    if request.method == 'GET':
        application_id = request.GET["id"]
        application = Application.objects.get(pk=application_id)
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
        temp_context = application_status_context
        del temp_context['declaration_status']
        # Enable/disable Declarations and Confirm your details tasks depending on task completion
        if ('NOT_STARTED' in temp_context.values()) or ('IN_PROGRESS' in temp_context.values()):
            application_status_context['all_complete'] = False
        else:
            application_status_context['all_complete'] = True
            application_status_context['declaration_status'] = application.declarations_status
            if application_status_context['declaration_status'] == 'COMPLETED':
                application_status_context['confirm_details'] = True
            else:
                application_status_context['confirm_details'] = False
    return render(request, 'task-list.html', application_status_context)


def personal_details_guidance(request):
    """
    Method returning the template for the Your personal details: guidance page (for a given application)
    and navigating to the Your login and contact details: name page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: guidance template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = PersonalDetailsGuidanceForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'personal_details_status': application.personal_details_status
        }
        return render(request, 'personal-details-guidance.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PersonalDetailsGuidanceForm(request.POST)
        if form.is_valid():
            if Application.objects.get(pk=application_id_local).personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            return HttpResponseRedirect(settings.URL_PREFIX + '/personal-details/name?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'personal-details-guidance.html', variables)


def personal_details_name(request):
    """
    Method returning the template for the Your personal details: name page (for a given application)
    and navigating to the Your personal details: date of birth page when successfully completed;
    business logic is applied to either create or update the associated Applicant_Name record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: name template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = PersonalDetailsNameForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'personal_details_status': application.personal_details_status
        }
        return render(request, 'personal-details-name.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PersonalDetailsNameForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            # Create or update Applicant_Names record
            applicant_names_record = personal_name_logic(application_id_local, form)
            applicant_names_record.save()
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/personal-details/dob/?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'personal-details-name.html', variables)


def personal_details_dob(request):
    """
    Method returning the template for the Your personal details: date of birth page (for a given application)
    and navigating to the Your personal details: home address page when successfully completed;
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: date of birth template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = PersonalDetailsDOBForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'personal_details_status': application.personal_details_status
        }
        return render(request, 'personal-details-dob.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PersonalDetailsDOBForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            # Update Applicant_Personal_Details record
            personal_details_record = personal_dob_logic(application_id_local, form)
            personal_details_record.save()
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(
                settings.URL_PREFIX + '/personal-details/home-address?id=' + application_id_local + '&manual=False')
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'personal-details-dob.html', variables)


def personal_details_home_address(request):
    """
    Method returning the template for the Your personal details: home address page (for a given application)
    and navigating to the Your personal details: location of care page when successfully completed;
    business logic is applied to either create or update the associated Applicant_Name record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: home address template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        application = Application.objects.get(pk=application_id_local)
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = PersonalDetailsHomeAddressForm(id=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'personal_details_status': application.personal_details_status
            }
            return render(request, 'personal-details-home-address.html', variables)
        elif manual == 'True':
            form = PersonalDetailsHomeAddressManualForm(id=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'personal_details_status': application.personal_details_status
            }
            return render(request, 'personal-details-home-address-manual.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        application = Application.objects.get(pk=application_id_local)
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = PersonalDetailsHomeAddressForm(request.POST, id=application_id_local)
            if form.is_valid():
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/personal-details/home-address/?id=' + application_id_local +
                    '&manual=False')
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'personal_details_status': application.personal_details_status
                }
                return render(request, 'personal-details-home-address.html', variables)
        if manual == 'True':
            form = PersonalDetailsHomeAddressManualForm(request.POST, id=application_id_local)
            if form.is_valid():
                if Application.objects.get(pk=application_id_local).personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                # Create or update Application_Home_Address record
                home_address_record = personal_home_address_logic(application_id_local, form)
                home_address_record.save()
                application.date_updated = current_date
                application.save()
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/personal-details/location-of-care?id=' + application_id_local)
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'personal_details_status': application.personal_details_status
                }
                return render(request, 'personal-details-home-address-manual.html', variables)


def personal_details_location_of_care(request):
    """
    Method returning the template for the Your personal details: location of care page (for a given application)
    and navigating to the Your personal details: childcare or summary page when successfully completed;
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: location of care template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=application_id_local).personal_detail_id
        applicant_home_address = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                  current_address=True)
        # Delete childcare address if it is marked the same as the home address
        multiple_childcare_address_logic(personal_detail_id)
        street_line1 = applicant_home_address.street_line1
        street_line2 = applicant_home_address.street_line2
        town = applicant_home_address.town
        county = applicant_home_address.county
        postcode = applicant_home_address.postcode
        application = Application.objects.get(pk=application_id_local)
        if application.login_details_status != 'COMPLETED':
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
        form = PersonalDetailsLocationOfCareForm(id=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'street_line1': street_line1,
            'street_line2': street_line2,
            'town': town,
            'county': county,
            'postcode': postcode,
            'personal_details_status': application.login_details_status
        }
        return render(request, 'personal-details-location-of-care.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=application_id_local).personal_detail_id
        form = PersonalDetailsLocationOfCareForm(request.POST, id=application_id_local)
        if form.is_valid():
            application = Application.objects.get(pk=application_id_local)
            if application.personal_details_status != 'COMPLETED':
                status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
            # Update home address record
            home_address_record = personal_location_of_care_logic(application_id_local, form)
            home_address_record.save()
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            # Delete childcare address if it is marked the same as the home address
            multiple_childcare_address_logic(personal_detail_id)
            if home_address_record.childcare_address == 'True':
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/personal-details/summary?id=' + application_id_local)
            elif home_address_record.childcare_address == 'False':
                return HttpResponseRedirect(settings.URL_PREFIX + '/personal-details/childcare-address?id=' +
                                            application_id_local + '&manual=False')
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'personal-details-location-of-care.html', variables)


def personal_details_childcare_address(request):
    """
    Method returning the template for the Your personal details: childcare address page (for a given application)
    and navigating to the Your personal details: summary page when successfully completed;
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: childcare template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = PersonalDetailsChildcareAddressForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'personal_details_status': application.personal_details_status
            }
            return render(request, 'personal-details-childcare-address.html', variables)
        elif manual == 'True':
            form = PersonalDetailsChildcareAddressManualForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'personal_details_status': application.personal_details_status
            }
            return render(request, 'personal-details-childcare-address-manual.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = PersonalDetailsChildcareAddressForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                if Application.objects.get(pk=application_id_local).personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                return HttpResponseRedirect(settings.URL_PREFIX +
                                            '/personal-details/childcare-address/?id=' + application_id_local +
                                            '&manual=False')
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'personal_details_status': application.personal_details_status
                }
                return render(request, 'personal-details-childcare-address.html', variables)
        if manual == 'True':
            form = PersonalDetailsChildcareAddressManualForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                application = Application.objects.get(pk=application_id_local)
                if application.personal_details_status != 'COMPLETED':
                    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
                # Update Applicant_Home_Address record
                childcare_address_record = personal_childcare_address_logic(application_id_local, form)
                childcare_address_record.save()
                application.date_updated = current_date
                application.save()
                return HttpResponseRedirect(
                    settings.URL_PREFIX + '/personal-details/summary?id=' + application_id_local)
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'personal_details_status': application.personal_details_status
                }
                return render(request, 'personal-details-childcare-address-manual.html', variables)


def personal_details_summary(request):
    """
    Method returning the template for the Your personal details: summary page (for a given application)
    displaying entered data for this task and navigating to the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your personal details: summary template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=application_id_local)
        birth_day = personal_detail_id.birth_day
        birth_month = personal_detail_id.birth_month
        birth_year = personal_detail_id.birth_year
        applicant_name_record = ApplicantName.objects.get(personal_detail_id=personal_detail_id)
        first_name = applicant_name_record.first_name
        middle_names = applicant_name_record.middle_names
        last_name = applicant_name_record.last_name
        applicant_home_address_record = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                         current_address=True)
        street_line1 = applicant_home_address_record.street_line1
        street_line2 = applicant_home_address_record.street_line2
        town = applicant_home_address_record.town
        county = applicant_home_address_record.county
        postcode = applicant_home_address_record.postcode
        location_of_childcare = applicant_home_address_record.childcare_address
        applicant_childcare_address_record = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                              childcare_address=True)
        childcare_street_line1 = applicant_childcare_address_record.street_line1
        childcare_street_line2 = applicant_childcare_address_record.street_line2
        childcare_town = applicant_childcare_address_record.town
        childcare_county = applicant_childcare_address_record.county
        childcare_postcode = applicant_childcare_address_record.postcode
        form = PersonalDetailsSummaryForm()
        application = Application.objects.get(pk=application_id_local)
        status.update(application_id_local, 'personal_details_status', 'COMPLETED')
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_name': first_name,
            'middle_names': middle_names,
            'last_name': last_name,
            'birth_day': birth_day,
            'birth_month': birth_month,
            'birth_year': birth_year,
            'street_line1': street_line1,
            'street_line2': street_line2,
            'town': town,
            'county': county,
            'postcode': postcode,
            'location_of_childcare': location_of_childcare,
            'childcare_street_line1': childcare_street_line1,
            'childcare_street_line2': childcare_street_line2,
            'childcare_town': childcare_town, 'childcare_county': childcare_county,
            'childcare_postcode': childcare_postcode,
            'personal_details_status': application.personal_details_status
        }
        return render(request, 'personal-details-summary.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PersonalDetailsSummaryForm()
        if form.is_valid():
            status.update(application_id_local, 'personal_details_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'personal-details-summary.html', variables)


def first_aid_training_guidance(request):
    """
    Method returning the template for the First aid training: guidance page (for a given application)
    and navigating to the First aid training: details page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: guidance template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstAidTrainingGuidanceForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-guidance.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingGuidanceForm(request.POST)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.first_aid_training_status != 'COMPLETED':
                status.update(application_id_local, 'first_aid_training_status', 'IN_PROGRESS')
            return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/details?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-training-guidance.html', variables)


def first_aid_training_details(request):
    """
    Method returning the template for the First aid training: details page (for a given application)
    and navigating to the First aid training: renew, declaration or training page depending on
    the age of the first aid training certificate when successfully completed;
    business logic is applied to either create or update the associated First_Aid_Training record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: details template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstAidTrainingDetailsForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-details.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingDetailsForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.first_aid_training_status != 'COMPLETED':
                status.update(application_id_local, 'first_aid_training_status', 'IN_PROGRESS')
            # Create or update First_Aid_Training record
            first_aid_training_record = first_aid_logic(application_id_local, form)
            first_aid_training_record.save()
            application.date_updated = current_date
            application.save()
            # Calculate certificate age and determine which page to navigate to
            certificate_day = form.cleaned_data['course_date'].day
            certificate_month = form.cleaned_data['course_date'].month
            certificate_year = form.cleaned_data['course_date'].year
            certificate_date = date(certificate_year, certificate_month, certificate_day)
            today = date.today()
            certificate_age = today.year - certificate_date.year - (
                    (today.month, today.day) < (certificate_date.month, certificate_date.day))
            if certificate_age < 2.5:
                return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/declaration?id=' + application_id_local)
            elif 2.5 <= certificate_age <= 3:
                return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/renew?id=' + application_id_local)
            elif certificate_age > 3:
                return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/training?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-details.html', variables)


def first_aid_training_declaration(request):
    """
    Method returning the template for the First aid training: declaration page (for a given application)
    and navigating to the First aid training: summary page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: declaration template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstAidTrainingDeclarationForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-declaration.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingDeclarationForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'first_aid_training_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-declaration.html', variables)


def first_aid_training_renew(request):
    """
    Method returning the template for the First aid training: renew page (for a given application)
    and navigating to the First aid training: summary page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: renew template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstAidTrainingRenewForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-renew.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingRenewForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'first_aid_training_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-renew.html', variables)


def first_aid_training_training(request):
    """
    Method returning the template for the First aid training: training page (for a given application)
    and navigating to the First aid training: summary page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: training template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstAidTrainingTrainingForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-training.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingTrainingForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'first_aid_training_status', 'NOT_STARTED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/first-aid/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-training.html', variables)


def first_aid_training_summary(request):
    """
    Method returning the template for the First aid training: summary page (for a given application)
    displaying entered data for this task and navigating to the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered First aid training: summary template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        training_organisation = FirstAidTraining.objects.get(application_id=application_id_local).training_organisation
        training_course = FirstAidTraining.objects.get(application_id=application_id_local).course_title
        certificate_day = FirstAidTraining.objects.get(application_id=application_id_local).course_day
        certificate_month = FirstAidTraining.objects.get(application_id=application_id_local).course_month
        certificate_year = FirstAidTraining.objects.get(application_id=application_id_local).course_year
        form = FirstAidTrainingSummaryForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'training_organisation': training_organisation,
            'training_course': training_course,
            'certificate_day': certificate_day,
            'certificate_month': certificate_month,
            'certificate_year': certificate_year,
            'first_aid_training_status': application.first_aid_training_status
        }
        return render(request, 'first-aid-summary.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstAidTrainingSummaryForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'first-aid-summary.html', variables)


def eyfs(request):
    """
    Method returning the template for the Early Years knowledge page (for a given application) and navigating to
    the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Early Years knowledge template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = EYFSForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'eyfs_training_status': application.eyfs_training_status
        }
        if application.eyfs_training_status != 'COMPLETED':
            status.update(application_id_local, 'eyfs_training_status', 'IN_PROGRESS')
        return render(request, 'eyfs.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = EYFSForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'eyfs_training_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'eyfs.html', variables)


def dbs_check_guidance(request):
    """
    Method returning the template for the Your criminal record (DBS) check: guidance page (for a given application)
    and navigating to the Your criminal record (DBS) check: details page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your criminal record (DBS) check: guidance template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = DBSCheckGuidanceForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'criminal_record_check_status': application.criminal_record_check_status
        }
        return render(request, 'dbs-check-guidance.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = DBSCheckGuidanceForm(request.POST)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.criminal_record_check_status != 'COMPLETED':
                status.update(application_id_local, 'criminal_record_check_status', 'IN_PROGRESS')
            return HttpResponseRedirect(settings.URL_PREFIX + '/dbs-check/dbs-details?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'dbs-check-guidance.html', variables)


def dbs_check_dbs_details(request):
    """
    Method returning the template for the Your criminal record (DBS) check: details page (for a given application)
    and navigating to the Your criminal record (DBS) check: upload DBS or summary page when successfully completed;
    business logic is applied to either create or update the associated Criminal_Record_Check record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your criminal record (DBS) check: details template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = DBSCheckDBSDetailsForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'criminal_record_check_status': application.criminal_record_check_status
        }
        return render(request, 'dbs-check-dbs-details.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = DBSCheckDBSDetailsForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.criminal_record_check_status != 'COMPLETED':
                status.update(application_id_local, 'criminal_record_check_status', 'IN_PROGRESS')
            # Create or update Criminal_Record_Check record
            dbs_check_record = dbs_check_logic(application_id_local, form)
            dbs_check_record.save()
            application.date_updated = current_date
            application.save()
            cautions_convictions = form.cleaned_data['convictions']
            if cautions_convictions == 'True':
                return HttpResponseRedirect(settings.URL_PREFIX + '/dbs-check/upload-dbs?id=' + application_id_local)
            elif cautions_convictions == 'False':
                if application.criminal_record_check_status != 'COMPLETED':
                    status.update(application_id_local, 'criminal_record_check_status', 'COMPLETED')
                return HttpResponseRedirect(settings.URL_PREFIX + '/dbs-check/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'dbs-check-dbs-details.html', variables)


def dbs_check_upload_dbs(request):
    """
    Method returning the template for the Your criminal record (DBS) check: upload DBS page (for a given application)
    and navigating to the Your criminal record (DBS) check: summary page when successfully completed;
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your criminal record (DBS) check: upload DBS template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = DBSCheckUploadDBSForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'criminal_record_check_status': application.criminal_record_check_status
        }
        return render(request, 'dbs-check-upload-dbs.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = DBSCheckUploadDBSForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            declare = form.cleaned_data['declaration']
            dbs_check_record = CriminalRecordCheck.objects.get(application_id=application_id_local)
            dbs_check_record.send_certificate_declare = declare
            dbs_check_record.save()
            application.date_updated = current_date
            application.save()
            if application.criminal_record_check_status != 'COMPLETED':
                status.update(application_id_local, 'criminal_record_check_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/dbs-check/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'dbs-check-upload-dbs.html', variables)


def dbs_check_summary(request):
    """
    Method returning the template for the Your criminal record (DBS) check: summary page (for a given application)
    displaying entered data for this task and navigating to the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your criminal record (DBS) check: summary template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        criminal_record_check = CriminalRecordCheck.objects.get(application_id=application_id_local)
        dbs_certificate_number = criminal_record_check.dbs_certificate_number
        cautions_convictions = criminal_record_check.cautions_convictions
        send_certificate_declare = criminal_record_check.send_certificate_declare
        form = DBSCheckSummaryForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'dbs_certificate_number': dbs_certificate_number,
            'cautions_convictions': cautions_convictions,
            'criminal_record_check_status': application.criminal_record_check_status,
            'declaration': send_certificate_declare
        }
        return render(request, 'dbs-check-summary.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = DBSCheckSummaryForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'dbs-check-summary.html', variables)


def health_intro(request):
    """
    Method returning the template for the Your health: intro page (for a given application)
    and navigating to the Your health: intro page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your health: intro template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = HealthIntroForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'health_status': application.health_status
        }
        return render(request, 'health-intro.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = HealthIntroForm(request.POST)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.health_status != 'COMPLETED':
                status.update(application_id_local, 'health_status', 'IN_PROGRESS')
            return HttpResponseRedirect(settings.URL_PREFIX + '/health/booklet?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'health-intro.html', variables)


def health_booklet(request):
    """
    Method returning the template for the Your health: booklet page (for a given application)
    and navigating to the Your health: answers page when successfully completed;
    business logic is applied to either create or update the associated Health_Declaration_Booklet record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your health: booklet template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = HealthBookletForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'health_status': application.health_status
        }
        return render(request, 'health-booklet.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = HealthBookletForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            # Create or update Health_Declaration_Booklet record
            hdb_record = health_check_logic(application_id_local, form)
            hdb_record.save()
            application.date_updated = current_date
            application.save()
            if application.health_status != 'COMPLETED':
                status.update(application_id_local, 'health_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/health/check-answers?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'health-booklet.html', variables)


def health_check_answers(request):
    """
    Method returning the template for the Your health: answers page (for a given application)
    displaying entered data for this task and navigating to the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Your health: answers template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        send_hdb_declare = HealthDeclarationBooklet.objects.get(application_id=application_id_local).send_hdb_declare
        form = HealthBookletForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'send_hdb_declare': send_hdb_declare,
            'health_status': application.health_status,
        }
        return render(request, 'health-check-answers.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = HealthBookletForm(request.POST, id=application_id_local)
        if form.is_valid():
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'health-check-answers.html', variables)


def references_intro(request):
    """
    Method returning the template for the 2 references: intro page (for a given application)
    and navigating to the Your health: intro page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: intro template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ReferenceIntroForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'references_status': application.references_status
        }
        return render(request, 'references-intro.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ReferenceIntroForm(request.POST)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.references_status != 'COMPLETED':
                status.update(application_id_local, 'references_status', 'IN_PROGRESS')
            return HttpResponseRedirect(settings.URL_PREFIX + '/references/first-reference?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-intro.html', variables)


def references_first_reference(request):
    """
    Method returning the template for the 2 references: first reference page (for a given application)
    and navigating to the 2 references: first reference address page when successfully completed;
    business logic is applied to either create or update the associated Reference record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: first reference template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = FirstReferenceForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'references_status': application.references_status
        }
        return render(request, 'references-first-reference.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = FirstReferenceForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.references_status != 'COMPLETED':
                status.update(application_id_local, 'references_status', 'IN_PROGRESS')
            # Create or update Reference record
            references_record = references_first_reference_logic(application_id_local, form)
            references_record.save()
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/references/first-reference-address?id='
                                        + application_id_local + '&manual=False')
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-first-reference.html', variables)


def references_first_reference_address(request):
    """
    Method returning the template for the 2 references: first reference address page (for a given application)
    and navigating to the 2 references: first reference contact details page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: first reference address template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        # Switch between manual address entry or postcode search
        if manual == 'False':
            form = ReferenceFirstReferenceAddressForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'references_status': application.references_status
            }
            return render(request, 'references-first-reference-address.html', variables)
        elif manual == 'True':
            form = ReferenceFirstReferenceAddressManualForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'references_status': application.references_status
            }
            return render(request, 'references-first-reference-address-manual.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        if manual == 'False':
            form = ReferenceFirstReferenceAddressForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                return HttpResponseRedirect(settings.URL_PREFIX + '/references/first-reference-address/?id='
                                            + application_id_local + '&manual=False')
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'references_status': application.references_status
                }
                return render(request, 'references-first-reference-address.html', variables)
        if manual == 'True':
            form = ReferenceFirstReferenceAddressManualForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                street_line1 = form.cleaned_data.get('street_name_and_number')
                street_line2 = form.cleaned_data.get('street_name_and_number2')
                town = form.cleaned_data.get('town')
                county = form.cleaned_data.get('county')
                country = form.cleaned_data.get('country')
                postcode = form.cleaned_data.get('postcode')
                # Create or update Reference record
                references_first_reference_address_record = Reference.objects.get(application_id=application_id_local,
                                                                                  reference=1)
                references_first_reference_address_record.street_line1 = street_line1
                references_first_reference_address_record.street_line2 = street_line2
                references_first_reference_address_record.town = town
                references_first_reference_address_record.county = county
                references_first_reference_address_record.country = country
                references_first_reference_address_record.postcode = postcode
                references_first_reference_address_record.save()
                application = Application.objects.get(pk=application_id_local)
                application.date_updated = current_date
                application.save()
                if application.references_status != 'COMPLETED':
                    status.update(application_id_local, 'references_status', 'IN_PROGRESS')
                return HttpResponseRedirect(settings.URL_PREFIX + '/references/first-reference-contact-details?id='
                                            + application_id_local)
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'references_status': application.references_status
                }
                return render(request, 'references-first-reference-address-manual.html', variables)


def references_first_reference_contact_details(request):
    """
    Method returning the template for the 2 references: first reference contact details page (for a given application)
    and navigating to the 2 references: second reference page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: first reference contact details template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ReferenceFirstReferenceContactForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'references_status': application.references_status
        }
        return render(request, 'references-first-reference-contact-details.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ReferenceFirstReferenceContactForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.references_status != 'COMPLETED':
                status.update(application_id_local, 'references_status', 'IN_PROGRESS')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            references_first_reference_address_record = Reference.objects.get(application_id=application_id_local,
                                                                              reference=1)
            references_first_reference_address_record.phone_number = phone_number
            references_first_reference_address_record.email = email_address
            references_first_reference_address_record.save()
            application = Application.objects.get(pk=application_id_local)
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/references/second-reference?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-first-reference-contact-details.html', variables)


def references_second_reference(request):
    """
    Method returning the template for the 2 references: second reference page (for a given application)
    and navigating to the 2 references: second reference address page when successfully completed;
    business logic is applied to either create or update the associated Reference record
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: second reference template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = SecondReferenceForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'references_status': application.references_status
        }
        return render(request, 'references-second-reference.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = SecondReferenceForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            if application.references_status != 'COMPLETED':
                status.update(application_id_local, 'references_status', 'IN_PROGRESS')
            # Create or update Reference record
            references_record = references_second_reference_logic(application_id_local, form)
            references_record.save()
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/references/second-reference-address?id=' +
                                        application_id_local + '&manual=False')
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-second-reference.html', variables)


def references_second_reference_address(request):
    """
    Method returning the template for the 2 references: second reference address page (for a given application)
    and navigating to the 2 references: second reference contact details page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: second reference address template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        manual = request.GET["manual"]
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = ReferenceSecondReferenceAddressForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'references_status': application.references_status
            }
            return render(request, 'references-second-reference-address.html', variables)
        elif manual == 'True':
            form = ReferenceSecondReferenceAddressManualForm(id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            variables = {
                'form': form,
                'application_id': application_id_local,
                'references_status': application.references_status
            }
            return render(request, 'references-second-reference-address-manual.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        manual = request.POST["manual"]
        # Switch between manual address entry and postcode search
        if manual == 'False':
            form = ReferenceSecondReferenceAddressForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                return HttpResponseRedirect(settings.URL_PREFIX + '/references/second-reference-address/?id='
                                            + application_id_local + '&manual=False')
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'references_status': application.references_status
                }
                return render(request, 'references-second-reference-address.html', variables)
        if manual == 'True':
            form = ReferenceSecondReferenceAddressManualForm(request.POST, id=application_id_local)
            application = Application.objects.get(pk=application_id_local)
            if form.is_valid():
                street_line1 = form.cleaned_data.get('street_name_and_number')
                street_line2 = form.cleaned_data.get('street_name_and_number2')
                town = form.cleaned_data.get('town')
                county = form.cleaned_data.get('county')
                country = form.cleaned_data.get('country')
                postcode = form.cleaned_data.get('postcode')
                if application.references_status != 'COMPLETED':
                    status.update(application_id_local, 'references_status', 'IN_PROGRESS')
                references_second_reference_address_record = Reference.objects.get(application_id=application_id_local,
                                                                                   reference=2)
                references_second_reference_address_record.street_line1 = street_line1
                references_second_reference_address_record.street_line2 = street_line2
                references_second_reference_address_record.town = town
                references_second_reference_address_record.county = county
                references_second_reference_address_record.country = country
                references_second_reference_address_record.postcode = postcode
                references_second_reference_address_record.save()
                application = Application.objects.get(pk=application_id_local)
                application.date_updated = current_date
                application.save()
                return HttpResponseRedirect(settings.URL_PREFIX + '/references/second-reference-contact-details?id='
                                            + application_id_local)
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'references_status': application.references_status
                }
                return render(request, 'references-second-reference-address-manual.html', variables)


def references_second_reference_contact_details(request):
    """
    Method returning the template for the 2 references: second reference contact details page (for a given application)
    and navigating to the 2 references: summary page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: second reference contact details template
    """
    current_date = datetime.datetime.today()
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ReferenceSecondReferenceContactForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'references_status': application.references_status
        }
        return render(request, 'references-second-reference-contact-details.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ReferenceSecondReferenceContactForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        if form.is_valid():
            status.update(application_id_local, 'references_status', 'COMPLETED')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            references_first_reference_address_record = Reference.objects.get(application_id=application_id_local,
                                                                              reference=2)
            references_first_reference_address_record.phone_number = phone_number
            references_first_reference_address_record.email = email_address
            references_first_reference_address_record.save()
            application.date_updated = current_date
            application.save()
            return HttpResponseRedirect(settings.URL_PREFIX + '/references/summary?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-second-reference-contact-details.html', variables)


def references_summary(request):
    """
    Method returning the template for the 2 references: summary page (for a given application)
    displaying entered data for this task and navigating to the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered 2 references: summary template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        first_reference_record = Reference.objects.get(application_id=application_id_local, reference=1)
        second_reference_record = Reference.objects.get(application_id=application_id_local, reference=2)
        first_reference_first_name = first_reference_record.first_name
        first_reference_last_name = first_reference_record.last_name
        first_reference_relationship = first_reference_record.relationship
        first_reference_years_known = first_reference_record.years_known
        first_reference_months_known = first_reference_record.months_known
        first_reference_street_line1 = first_reference_record.street_line1
        first_reference_street_line2 = first_reference_record.street_line2
        first_reference_town = first_reference_record.town
        first_reference_county = first_reference_record.county
        first_reference_country = first_reference_record.country
        first_reference_postcode = first_reference_record.postcode
        first_reference_phone_number = first_reference_record.phone_number
        first_reference_email = first_reference_record.email
        second_reference_first_name = second_reference_record.first_name
        second_reference_last_name = second_reference_record.last_name
        second_reference_relationship = second_reference_record.relationship
        second_reference_years_known = second_reference_record.years_known
        second_reference_months_known = second_reference_record.months_known
        second_reference_street_line1 = second_reference_record.street_line1
        second_reference_street_line2 = second_reference_record.street_line2
        second_reference_town = second_reference_record.town
        second_reference_county = second_reference_record.county
        second_reference_country = second_reference_record.country
        second_reference_postcode = second_reference_record.postcode
        second_reference_phone_number = second_reference_record.phone_number
        second_reference_email = second_reference_record.email
        form = ReferenceSummaryForm()
        application = Application.objects.get(pk=application_id_local)
        status.update(application_id_local, 'references_status', 'COMPLETED')
        variables = {
            'form': form,
            'application_id': application_id_local,
            'first_reference_first_name': first_reference_first_name,
            'first_reference_last_name': first_reference_last_name,
            'first_reference_relationship': first_reference_relationship,
            'first_reference_years_known': first_reference_years_known,
            'first_reference_months_known': first_reference_months_known,
            'first_reference_street_line1': first_reference_street_line1,
            'first_reference_street_line2': first_reference_street_line2,
            'first_reference_town': first_reference_town,
            'first_reference_county': first_reference_county,
            'first_reference_country': first_reference_country,
            'first_reference_postcode': first_reference_postcode,
            'first_reference_phone_number': first_reference_phone_number,
            'first_reference_email': first_reference_email,
            'second_reference_first_name': second_reference_first_name,
            'second_reference_last_name': second_reference_last_name,
            'second_reference_relationship': second_reference_relationship,
            'second_reference_years_known': second_reference_years_known,
            'second_reference_months_known': second_reference_months_known,
            'second_reference_street_line1': second_reference_street_line1,
            'second_reference_street_line2': second_reference_street_line2,
            'second_reference_town': second_reference_town,
            'second_reference_county': second_reference_county,
            'second_reference_country': second_reference_country,
            'second_reference_postcode': second_reference_postcode,
            'second_reference_phone_number': second_reference_phone_number,
            'second_reference_email': second_reference_email,
            'references_status': application.references_status
        }
        return render(request, 'references-summary.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PersonalDetailsSummaryForm()
        if form.is_valid():
            status.update(application_id_local, 'references_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'references-summary.html', variables)


def other_people(request):
    """
    Method returning the template for the People in your home page (for a given application) and navigating to
    the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered People in your home template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = OtherPeopleForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'people_in_home_status': application.people_in_home_status
        }
        if application.people_in_home_status != 'COMPLETED':
            status.update(application_id_local, 'people_in_home_status', 'IN_PROGRESS')
        return render(request, 'other-people.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = OtherPeopleForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'people_in_home_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'other-people.html', variables)


def declaration(request):
    """
    Method returning the template for the Declaration page (for a given application) and navigating to
    the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Declaration template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = DeclarationForm()
        application = Application.objects.get(pk=application_id_local)
        variables = {
            'form': form,
            'application_id': application_id_local,
            'declarations_status': application.declarations_status
        }
        # Set task to completed, as form is still to be created in later sprint
        if application.declarations_status != 'COMPLETED':
            status.update(application_id_local, 'declarations_status', 'COMPLETED')
        return render(request, 'declaration.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = DeclarationForm(request.POST)
        if form.is_valid():
            status.update(application_id_local, 'declarations_status', 'COMPLETED')
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'declaration.html', variables)


def confirmation(request):
    """
    Method returning the template for the Confirmation page (for a given application) and navigating to
    the task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Confirmation template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ConfirmForm()
        variables = {
            'form': form,
            'application_id': application_id_local,
        }
        return render(request, 'confirm.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ConfirmForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(settings.URL_PREFIX + '/task-list?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'confirm.html', variables)


def payment_selection(request):
    """
    Method returning the template for the Payment page (for a given application) and navigating to
    the card payment details page or PayPal site when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Payment template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        paid = Application.objects.get(pk=application_id_local).order_code
        print(paid)
        if paid is None:
            form = PaymentForm()
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'payment.html', variables)
        elif paid is not None:
            variables = {
                'application_id': application_id_local,
                'order_code': paid
            }
            return render(request, 'paid.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            application_url_base = settings.PUBLIC_APPLICATION_URL
            if payment_method == 'Credit':
                return HttpResponseRedirect(settings.URL_PREFIX + '/payment-details/?id=' + application_id_local)
            elif payment_method == 'PayPal':
                paypal_url = payment.make_paypal_payment("GB", 3500, "GBP", "Childminder Registration Fee",
                                                         application_id_local, application_url_base +
                                                         "/paypal-payment-completion/?id=" + application_id_local,

                                                         application_url_base +
                                                         "/payment/?id=" + application_id_local,

                                                         application_url_base +
                                                         "/payment/?id=" + application_id_local,

                                                         application_url_base +
                                                         "/payment/?id=" + application_id_local)
                return HttpResponseRedirect(paypal_url)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'payment.html', variables)


@never_cache
def card_payment_details(request):
    """
    Method returning the template for the Card payment details page (for a given application) and navigating to
    the payment confirmation page when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Card payment details template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        paid = Application.objects.get(pk=application_id_local).order_code
        print(paid)
        if paid is None:
            form = PaymentDetailsForm()
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'payment-details.html', variables)
        elif paid is not None:
            variables = {
                'application_id': application_id_local,
                'order_code': paid
            }
            return render(request, 'paid.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = PaymentDetailsForm(request.POST)
        if form.is_valid():
            card_number = re.sub('[ -]+', '', request.POST["card_number"])
            cardholders_name = request.POST["cardholders_name"]
            card_security_code = request.POST["card_security_code"]
            expiry_month = request.POST["expiry_date_0"]
            expiry_year = request.POST["expiry_date_1"]
            # Make payment
            payment_response = payment.make_payment(3500, cardholders_name, card_number, card_security_code,
                                                    expiry_month, expiry_year, 'GBP', application_id_local,
                                                    application_id_local)
            parsed_payment_response = json.loads(payment_response.text)
            # If the payment is successful
            if payment_response.status_code == 201:
                application = Application.objects.get(pk=application_id_local)
                login_id = application.login_id.login_id
                login_record = UserDetails.objects.get(pk=login_id)
                personal_detail_id = ApplicantPersonalDetails.objects.get(application_id=
                                                                          application_id_local).personal_detail_id
                applicant_name_record = ApplicantName.objects.get(personal_detail_id=personal_detail_id)
                payment.payment_email(login_record.email, applicant_name_record.first_name)
                print('Email sent')
                order_code = parsed_payment_response["orderCode"]
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'order_code': order_code
                }
                application.order_code = UUID(order_code)
                application.save()
                return HttpResponseRedirect(settings.URL_PREFIX + '/confirmation/?id=' + application_id_local +
                                            '&orderCode=' + order_code, variables)
            else:
                variables = {
                    'form': form,
                    'application_id': application_id_local,
                    'error_flag': 1,
                    'error_message': parsed_payment_response["message"],
                }
            return HttpResponseRedirect(settings.URL_PREFIX + '/payment-details/?id=' + application_id_local, variables)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'payment-details.html', variables)


def paypal_payment_completion(request):
    if request.method == 'GET':
        application_id_local = request.GET['id']
        order_code = request.GET['orderCode']
        # If the payment has been successfully processed
        if payment.check_payment(order_code) == 200:
            variables = {
                'application_id': application_id_local,
                'order_code': request.GET["orderCode"],
            }

            application = Application.objects.get(pk=application_id_local)
            application.order_code = UUID(order_code)
            application.save()

            return HttpResponseRedirect(settings.URL_PREFIX + '/confirmation/?id=' + application_id_local +
                                        '&orderCode=' + order_code, variables)
        else:
            print('HELP')
            return render(request, '500.html')

def payment_confirmation(request):
    """
    Method returning the template for the Payment confirmation page (for a given application)
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Payment confirmation template
    """
    if request.method == 'GET':
        application_id_local = request.GET['id']
        order_code = request.GET['orderCode']
        # If the payment has been successfully processed
        if payment.check_payment(order_code) == 200:
            variables = {
                'application_id': application_id_local,
                'order_code': request.GET["orderCode"],
            }
            return render(request, 'payment-confirmation.html', variables)
        else:
            form = PaymentForm()
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return HttpResponseRedirect(settings.URL_PREFIX + '/payment/?id=' + application_id_local, variables)


def application_saved(request):
    """
    Method returning the template for the Application saved page (for a given application)
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Application saved template
    """
    if request.method == 'GET':
        application_id_local = request.GET["id"]
        form = ApplicationSavedForm()
        variables = {
            'form': form,
            'application_id': application_id_local,
        }
        return render(request, 'application-saved.html', variables)
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ApplicationSavedForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(settings.URL_PREFIX + '/application-saved/?id=' + application_id_local)
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            return render(request, 'application-saved.html', variables)
