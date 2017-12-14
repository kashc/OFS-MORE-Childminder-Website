'''
Created on 7 Dec 2017
@author: Informed Solutions
'''

from application.models import Application, Criminal_Record_Check, Login_And_Contact_Details, Applicant_Personal_Details, Applicant_Names, First_Aid_Training,\
    Health_Declaration_Booklet, References

from application import status

from django.template import Context
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import TypeOfChildcare, ContactEmail, DBSCheck, PersonalDetails, FirstAidTraining, EYFS, HealthDeclarationBooklet, OtherPeople, ReferenceForm

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
            'health_status': application.health_status,
            'reference_status': application.references_status,
            'people_in_home_status': application.people_in_home_status,
            'declaration_status': application.declarations_status,
            'all_complete': False,
            })
        
        temp_context = application_status_context
        del temp_context['declaration_status']
        print (temp_context)
        
        if ('NOT_STARTED' in temp_context.values()) or ('IN_PROGRESS' in temp_context.values()):
            application_status_context['all_complete'] = False
        else:
            application_status_context['all_complete'] = True

    return render(request, 'task-list.html', application_status_context)
        

def TypeOfChildcareView(request):
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = TypeOfChildcare(request.POST)
        
        if form.is_valid():
            
            status.update(application_id_local, 'childcare_type_status', 'COMPLETED')
            return HttpResponseRedirect('/task-list?id=' + application_id_local)
    else:
        application_id_local = request.GET["id"]
        status.update(application_id_local, 'childcare_type_status', 'IN_PROGRESS')
        form = TypeOfChildcare()
         
        return render(request, 'childcare.html', {'form': form, 'application_id': application_id_local})
    
#def ApplicationStatusView(request):
#    if request.method == 'GET':
#        
#        form = ApplicationStatus(request.POST)

def ContactEmailView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = ContactEmail(request.POST,id = application_id_local)
        
        if form.is_valid():
            
            status.update(application_id_local, 'login_details_status', 'COMPLETED')
            # If no record exists, create a new one
            if Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() == 0:
            
                login_and_contact_details_record = Login_And_Contact_Details(email=form.cleaned_data.get('email_address'), application_id=Application.objects.get(application_id=application_id_local))
                login_and_contact_details_record.save()
            
            # If a record exists, update it
            if Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() > 0:
                
                login_and_contact_details_record = Login_And_Contact_Details.objects.get(application_id=application_id_local)
                login_and_contact_details_record.email = form.cleaned_data.get('email_address')
                login_and_contact_details_record.save()
            
            return HttpResponseRedirect('/task-list?id=' + application_id_local)

    #print(request)
    application_id_local = request.GET["id"]
    status.update(application_id_local, 'login_details_status', 'IN_PROGRESS')
    form = ContactEmail(id = application_id_local)       
    return render(request, 'contact-email.html', {'form': form,'application_id': application_id_local})

def PersonalDetailsView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = PersonalDetails(request.POST, id = application_id_local)
        
        if form.is_valid():            
            
            status.update(application_id_local, 'personal_details_status', 'COMPLETED')
            
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
    status.update(application_id_local, 'personal_details_status', 'IN_PROGRESS')
    form = PersonalDetails(id = application_id_local)       
    return render(request, 'personal-details.html', {'form': form,'application_id': application_id_local})

def DBSCheckView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = DBSCheck(request.POST, id = application_id_local)
        
        if form.is_valid():
            
            status.update(application_id_local, 'criminal_record_check_status', 'COMPLETED')
            
            # If no record exists, create a new one
            if Criminal_Record_Check.objects.filter(application_id=application_id_local).count() == 0:
            
                c = Criminal_Record_Check(dbs_certificate_number=form.cleaned_data.get('dbs_certificate_number'), cautions_convictions=form.cleaned_data.get('convictions'), application_id=Application.objects.get(application_id=application_id_local))
                c.save()
            
            # If a record exists, update it
            elif Criminal_Record_Check.objects.filter(application_id=application_id_local).count() > 0:
                
                c = Criminal_Record_Check.objects.get(application_id=application_id_local)
                c.dbs_certificate_number = form.cleaned_data.get('dbs_certificate_number')
                c.cautions_convictions = form.cleaned_data.get('convictions')
                c.save()
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    application_id_local = request.GET["id"]
    
    status.update(application_id_local, 'criminal_record_check_status', 'IN_PROGRESS')

    form = DBSCheck(id = application_id_local)       
    return render(request, 'dbs-check.html', {'form': form,'application_id': application_id_local})

def FirstAidTrainingView(request):
    if request.method =='POST':
        application_id_local = request.POST["id"]
        form = FirstAidTraining(request.POST,id = application_id_local)
        
        if form.is_valid():
            
            status.update(application_id_local, 'first_aid_training_status', 'COMPLETED')
            
            # If no record exists, create a new one
            if First_Aid_Training.objects.filter(application_id=application_id_local).count() == 0:
                
                f = First_Aid_Training(training_organisation=form.cleaned_data.get('first_aid_training_organisation'),course_title=form.cleaned_data.get('title_of_training_course'), course_day=form.cleaned_data.get('course_date').day, course_month=form.cleaned_data.get('course_date').month, course_year=form.cleaned_data.get('course_date').year, application_id=Application.objects.get(application_id=application_id_local))
                f.save()
            
            # If a record exists, update it
            elif First_Aid_Training.objects.filter(application_id=application_id_local).count() > 0:
                
                f = First_Aid_Training.objects.get(application_id=application_id_local)
                f.training_organisation = form.cleaned_data.get('first_aid_training_organisation')
                f.course_title = form.cleaned_data.get('title_of_training_course')
                f.course_day = form.cleaned_data.get('course_date').day
                f.course_month = form.cleaned_data.get('course_date').month
                f.course_year = form.cleaned_data.get('course_date').year
                f.save()
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)

    application_id_local = request.GET["id"]
    status.update(application_id_local, 'first_aid_training_status', 'IN_PROGRESS')
    form = FirstAidTraining(id = application_id_local)       
    return render(request, 'first-aid.html', {'form': form,'application_id': application_id_local})

def EYFSView(request):
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = EYFS(request.POST)
        
        if form.is_valid():
            
            status.update(application_id_local, 'eyfs_training_status', 'COMPLETED')
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    application_id_local = request.GET["id"]
    status.update(application_id_local, 'eyfs_training_status', 'IN_PROGRESS')
    form = EYFS()
    
    return render(request, 'eyfs.html', {'application_id': application_id_local})

def OtherPeopleView(request):
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = OtherPeople(request.POST)
        
        if form.is_valid():
            
            status.update(application_id_local, 'people_in_home_status', 'COMPLETED')
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    application_id_local = request.GET["id"]
    status.update(application_id_local, 'people_in_home_status', 'IN_PROGRESS')
    form = OtherPeople()
    
    
    return render(request, 'other-people.html', {'application_id': application_id_local})

def ReferencesView(request):
    
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = ReferenceForm(request.POST,id = application_id_local)
        
        if form.is_valid():
            
            status.update(application_id_local, 'references_status', 'COMPLETED')
            
            # If no record exists, create a new one
            if References.objects.filter(application_id=application_id_local).count() == 0:
                
                r = References(first_name=form.cleaned_data.get('first_name'),last_name=form.cleaned_data.get('last_name'),relationship=form.cleaned_data.get('relationship'),years_known=0,months_known=0,street_line1='',street_line2='',town='',county='',country='',postcode='',phone_number='',email='',application_id=Application.objects.get(application_id=application_id_local))
                r.save()
            
            # If a record exists, update it
            elif References.objects.filter(application_id=application_id_local).count() > 0:
                
                r = References.objects.get(application_id=application_id_local)
                r.first_name = form.cleaned_data.get('first_name')
                r.last_name = form.cleaned_data.get('last_name')
                r.relationship = form.cleaned_data.get('relationship')
                r.save()
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    application_id_local = request.GET["id"]
    status.update(application_id_local, 'references_status', 'IN_PROGRESS')
    form = ReferenceForm(id = application_id_local)
    
    return render(request, 'references.html', {'form': form,'application_id': application_id_local})   

def HealthView(request):
    if request.method == 'POST':
        application_id_local = request.POST["id"]
        form = HealthDeclarationBooklet(request.POST, id = application_id_local)
        
        if form.is_valid():
            
            status.update(application_id_local, 'health_status', 'COMPLETED')
            
            # If no record exists, create a new one
            if Health_Declaration_Booklet.objects.filter(application_id=application_id_local).count() == 0:
                
                h = Health_Declaration_Booklet(movement_problems=form.cleaned_data.get('walking_bending'), breathing_problems=form.cleaned_data.get('asthma_breathing'), heart_disease=form.cleaned_data.get('heart_disease'), blackout_epilepsy=form.cleaned_data.get('blackout_epilepsy'), mental_health_problems=form.cleaned_data.get('mental_health'), alcohol_drug_problems=form.cleaned_data.get('alcohol_drugs'), application_id=Application.objects.get(application_id=application_id_local))
                h.save()
            
            # If a record exists, update it
            elif Health_Declaration_Booklet.objects.filter(application_id=application_id_local).count() > 0:
                
                h = Health_Declaration_Booklet.objects.get(application_id=application_id_local)
                h.movement_problems = form.cleaned_data.get('walking_bending')
                h.breathing_problems = form.cleaned_data.get('asthma_breathing')
                h.heart_disease = form.cleaned_data.get('heart_disease')
                h.blackout_epilepsy = form.cleaned_data.get('blackout_epilepsy')
                h.mental_health_problems = form.cleaned_data.get('mental_health')
                h.alcohol_drug_problems = form.cleaned_data.get('alcohol_drugs')
                h.save()
            
            return HttpResponseRedirect('/task-list/?id=' + application_id_local)
    
    application_id_local = request.GET["id"]
    status.update(application_id_local, 'health_status', 'IN_PROGRESS')
    form = HealthDeclarationBooklet(id = application_id_local)
    
    return render(request, 'health.html', {'form': form,'application_id': application_id_local})

def ResetView(request):
    SECTION_LIST = ['login_details_status', 'personal_details_status', 'childcare_type_status', 
                    'first_aid_training_status', 'eyfs_training_status', 'criminal_record_check_status'
                    , 'health_status', 'references_status', 'people_in_home_status', 'declarations_status']    
    application_id_local = request.GET["id"]
    
    for section in SECTION_LIST:
        status.update(application_id_local, section, 'NOT_STARTED')
        
    return HttpResponseRedirect('/task-list/?id=' + application_id_local)