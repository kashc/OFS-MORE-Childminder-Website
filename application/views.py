'''
Created on 7 Dec 2017
@author: Informed Solutions
'''

from application.models import Application, Criminal_Record_Check, Login_And_Contact_Details, Applicant_Personal_Details, Applicant_Names

from django.template import Context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import TypeOfChildcare, ContactEmail, DBSCheck, PersonalDetails, FirstAidTraining

def StartPageView(request):
    application = Application.objects.create(
        login_details_status = 'NOT_STARTED',
        personal_details_status = 'NOT_STARTED',
        childcare_type_status = 'NOT_STARTED',
        first_aid_training_status = 'NOT_STARTED',
        eyfs_training_status = 'NOT_STARTED',
        criminal_record_check_status = 'NOT_STARTED',
        health_status = 'NOT_STARTED',
        references_status = 'NOT_STARTED',
        people_in_home_status = 'NOT_STARTED',
        declarations_status = 'NOT_STARTED'
        )
    
    return render(request, 'start-page.html', ({'id': application.application_id}))


def LogInView(request):
           
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
            'health status': application.health_status,
            'reference_status': application.references_status,
            'people_in_home_status': application.people_in_home_status,
            'declaration_status': application.declarations_status,
            }) 
    return render(request, 'task-list.html', application_status_context)
        

def TypeOfChildcareView(request):
    if request.method == 'POST':

        form = TypeOfChildcare(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect('/task-list/?')
    else:
        form = TypeOfChildcare()
         
        return render(request, 'childcare.html', {'form': form})
    
#def ApplicationStatusView(request):
#    if request.method == 'GET':
#        
#        form = ApplicationStatus(request.POST)

def ContactEmailView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = ContactEmail(request.POST,id = application_id_local)
        
        if form.is_valid():
            print(form.cleaned_data)
            
            # If no record exists, create a new one
            if Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() == 0:
            
                login_and_contact_details_record = Login_And_Contact_Details(email=form.cleaned_data.get('email_address'), application_id=Application.objects.get(application_id=application_id_local))
                login_and_contact_details_record.save()
            
            # If a record exists, update it
            elif Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() > 0:
                
                login_and_contact_details_record = Login_And_Contact_Details.objects.get(application_id=application_id_local)
                login_and_contact_details_record.email = form.cleaned_data.get('email_address')
                login_and_contact_details_record.save()
            
            return HttpResponseRedirect('/task-list?id=' + application_id_local)

    #print(request)
    application_id_local = request.GET["id"]
    form = ContactEmail(id = application_id_local)       
    return render(request, 'contact-email.html', {'form': form,'application_id': application_id_local})

def PersonalDetailsView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = PersonalDetails(request.POST, id = application_id_local)
        
        if form.is_valid():            
            print(form.cleaned_data)
            
            # If no record exists, create a new one
            if Applicant_Personal_Details.objects.filter(application_id=application_id_local).count() == 0:
                
                personal_details_record = Applicant_Personal_Details(birth_day=0, birth_month=0, birth_year=0, application_id=Application.objects.get(application_id=application_id_local))
                personal_details_record.save()
                
                applicant_names_record = Applicant_Names(current_name='True', first_name=form.cleaned_data.get('first_name'), middle_names=form.cleaned_data.get('middle_names'), last_name=form.cleaned_data.get('last_name'), personal_detail_id=Applicant_Personal_Details.objects.get(application_id=application_id_local))
                applicant_names_record.save()
            
            # If a record exists, update it
            elif Applicant_Personal_Details.objects.filter(application_id=application_id_local).count() > 0:
                
                personal_detail_id_local = Applicant_Personal_Details.objects.get(application_id=application_id_local).personal_detail_id
                applicant_names_record = Applicant_Names.objects.get(personal_detail_id=personal_detail_id_local)
                applicant_names_record.first_name = form.cleaned_data.get('first_name')
                applicant_names_record.middle_names = form.cleaned_data.get('middle_names')
                applicant_names_record.last_name = form.cleaned_data.get('last_name')
                applicant_names_record.save()
            
            return HttpResponseRedirect('/task-list?id=' + application_id_local)


    application_id_local = request.GET["id"]
    form = PersonalDetails(id = application_id_local)       
    return render(request, 'personal-details.html', {'form': form})

def DBSCheckView(request):
    if request.method =='POST':
        
        form = DBSCheck(request.POST)
        
        if form.is_valid():
            
            print(form.cleaned_data)
            
            # If no record exists, create a new one
            if Criminal_Record_Check.objects.filter(application_id='48629508-b1d6-481f-b528-23538f4022d3').count() == 0:
            
                c = Criminal_Record_Check(dbs_certificate_number=form.cleaned_data.get('dbs_certificate_number'), cautions_convictions=form.cleaned_data.get('convictions'), application_id=Application.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3'))
                c.save()
            
            # If a record exists, update it
            elif Criminal_Record_Check.objects.filter(application_id='48629508-b1d6-481f-b528-23538f4022d3').count() > 0:
                
                c = Criminal_Record_Check.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3')
                c.dbs_certificate_number = form.cleaned_data.get('dbs_certificate_number')
                c.cautions_convictions = form.cleaned_data.get('convictions')
                c.save()
            
            return HttpResponseRedirect('/task-list/')

    form = DBSCheck()       
    return render(request, 'dbs-check.html', {'form': form})

def FirstAidTrainingView(request):
    if request.method =='POST':
        
        form = FirstAidTraining(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect('/task-list/')

    form = FirstAidTraining()       
    return render(request, 'first-aid.html', {'form': form})