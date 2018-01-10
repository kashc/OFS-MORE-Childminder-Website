"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Business Logic --

@author: Informed Solutions
"""


import datetime

from .models import (Applicant_Home_Address, Applicant_Names, ApplicantPersonalDetails, Application,
                     ChildcareType, Criminal_Record_Check, First_Aid_Training, Health_Declaration_Booklet,
                     References)


# Business logic to create or update a Type of childcare record
def ChildcareType_Logic(application_id_local, form):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into database
    zero_to_five_status = '0-5' in form.cleaned_data.get('type_of_childcare')
    five_to_eight_status = '5-8' in form.cleaned_data.get('type_of_childcare')
    eight_plus_status = '8over' in form.cleaned_data.get('type_of_childcare')
    
    # If the user entered information for this task for the first time
    if ChildcareType.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new Type of childcare record with the entered data
        childcare_type_record = ChildcareType(zero_to_five=zero_to_five_status, five_to_eight=five_to_eight_status, eight_plus=eight_plus_status, application_id=this_application)
            
    # If the user previously entered information for this task
    elif ChildcareType.objects.filter(application_id=application_id_local).count() > 0:
            
        # Retrieve the Type of childcare record corresponding to the application
        childcare_type_record = ChildcareType.objects.get(application_id=application_id_local)
        # Update the record
        childcare_type_record.zero_to_five = zero_to_five_status
        childcare_type_record.five_to_eight = five_to_eight_status
        childcare_type_record.eight_plus = eight_plus_status
    
    return childcare_type_record


# Business logic to create or update a Your login and contact details record: e-mail address
def Login_Contact_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)

    # Get entered data to insert into database
    email_address = form.cleaned_data.get('email_address')

    # Update user details record
    login_and_contact_details_record = this_application.login_id
    login_and_contact_details_record.email = email_address

    return login_and_contact_details_record


# Business logic to create or update a Your login and contact details record: phone numbers
def Login_Contact_Logic_Phone(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)

    # Get entered data to insert into database
    mobile_number = form.cleaned_data.get('mobile_number')
    add_phone_number = form.cleaned_data.get('add_phone_number')

    # Update user details record
    login_and_contact_details_record = this_application.login_id
    login_and_contact_details_record.mobile_number = mobile_number
    login_and_contact_details_record.add_phone_number = add_phone_number

    return login_and_contact_details_record


# Business logic to create or update a Your personal details record: names
def Personal_Name_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into the database
    first_name = form.cleaned_data.get('first_name')
    middle_names = form.cleaned_data.get('middle_names')
    last_name = form.cleaned_data.get('last_name')
    
    # If the user entered information for this task for the first time
    if ApplicantPersonalDetails.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new Applicant_Personal_Details record corresponding to the application, of which the generated personal_details_id will be used        
        personal_details_record = ApplicantPersonalDetails(birth_day=None, birth_month=None, birth_year=None, application_id=this_application)
        personal_details_record.save()
        personal_detail_id_local = ApplicantPersonalDetails.objects.get(application_id=application_id_local)
        
        # Create a new Your personal details record corresponding to the application    
        applicant_names_record = Applicant_Names(current_name='True', first_name=first_name, middle_names=middle_names, last_name=last_name, personal_detail_id=personal_detail_id_local)
            
    # If a record exists, update it
    elif ApplicantPersonalDetails.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the personal_details_id corresponding to the application       
        personal_detail_id_local = ApplicantPersonalDetails.objects.get(application_id=application_id_local).personal_detail_id
        # Retrieve the Your personal details record corresponding to the application
        applicant_names_record = Applicant_Names.objects.get(personal_detail_id=personal_detail_id_local)
        # Update the record
        applicant_names_record.first_name = first_name
        applicant_names_record.middle_names = middle_names
        applicant_names_record.last_name = last_name
    
    return applicant_names_record


# Business logic to create or update a Your personal details record: date of birth
def Personal_DOB_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into the database
    birth_day = form.cleaned_data.get('date_of_birth')[0]
    birth_month = form.cleaned_data.get('date_of_birth')[1]
    birth_year = form.cleaned_data.get('date_of_birth')[2]
    
    # If the user entered information for this task for the first time
    if ApplicantPersonalDetails.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new Your personal details record corresponding to the application         
        personal_details_record = ApplicantPersonalDetails(birth_day=birth_day, birth_month=birth_month, birth_year=birth_year, application_id=this_application)
        personal_details_record.save()
            
    # If a record exists, update it
    elif ApplicantPersonalDetails.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the Your personal details record corresponding to the application       
        personal_details_record = ApplicantPersonalDetails.objects.get(application_id=application_id_local)
        # Update the record
        personal_details_record.birth_day = birth_day
        personal_details_record.birth_month = birth_month
        personal_details_record.birth_year = birth_year
    
    return personal_details_record


# Business logic to create or update a Your personal details record: home address
def Personal_Home_Address_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into the database
    street_line1 = form.cleaned_data.get('street_name_and_number')
    street_line2 = form.cleaned_data.get('street_name_and_number2')
    town = form.cleaned_data.get('town')
    county = form.cleaned_data.get('county')
    postcode = form.cleaned_data.get('postcode')
    
    personal_detail_record = ApplicantPersonalDetails.objects.get(application_id=this_application)
    personal_detail_id = personal_detail_record.personal_detail_id
    
    # If the user entered information for this task for the first time
    if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id).count() == 0:
        
        # Create a new Applicant_Personal_Details record corresponding to the application, of which the generated personal_details_id will be used        
        home_address_record = Applicant_Home_Address(street_line1=street_line1, street_line2=street_line2, town=town, county=county, country='United Kingdom', postcode=postcode, childcare_address=None, current_address=True, move_in_month=0, move_in_year=0, personal_detail_id=personal_detail_record)
        home_address_record.save()
            
    # If a record exists, update it
    elif Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, current_address=True).count() > 0:
        
        # Retrieve the Your personal details record corresponding to the application
        home_address_record = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id, current_address=True)
        # Update the record
        home_address_record.street_line1 = street_line1
        home_address_record.street_line2 = street_line2
        home_address_record.town = town
        home_address_record.county = county
        home_address_record.postcode = postcode
    
    return home_address_record


# Business logic to create or update a Your personal details record: location of care
def Personal_Location_Of_Care_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into the database
    location_of_care = form.cleaned_data.get('location_of_care')
    
    personal_detail_record = ApplicantPersonalDetails.objects.get(application_id=this_application)
    personal_detail_id = personal_detail_record.personal_detail_id
        
    # Retrieve the Your personal details record corresponding to the application
    home_address_record = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id, current_address=True)
    # Update the record
    home_address_record.childcare_address = location_of_care
        
    return home_address_record


def Multiple_Childcare_Address_Logic(personal_detail_id):
    
    # Remove current address status from previously entered childcare address
    # If there are multiple addresses marked as the childcare address
    if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, childcare_address=True).count() > 1:
            
        # If the home address is marked as a childcare address
        if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, childcare_address=True, current_address=True).count() > 0:
            
            # If a non-home address is also marked as a childcare address
            if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, childcare_address=True, current_address=False).count() > 0:
                    
                # Retrieve the non-home address
                childcare_address_record = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id, childcare_address=True, current_address=False)
                # Delete the address
                childcare_address_record.delete()


# Business logic to create or update a Your personal details record: childcare address
def Personal_Childcare_Address_Logic(application_id_local, form):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into the database
    street_line1 = form.cleaned_data.get('street_name_and_number')
    street_line2 = form.cleaned_data.get('street_name_and_number2')
    town = form.cleaned_data.get('town')
    county = form.cleaned_data.get('county')
    postcode = form.cleaned_data.get('postcode')
    
    personal_detail_record = ApplicantPersonalDetails.objects.get(application_id=this_application)
    personal_detail_id = personal_detail_record.personal_detail_id
    
    # If the user entered information for this task for the first time
    if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, childcare_address='True').count() == 0:
        
        # Create a new Applicant_Personal_Details record corresponding to the application, of which the generated personal_details_id will be used        
        childcare_address_record = Applicant_Home_Address(street_line1=street_line1, street_line2=street_line2, town=town, county=county, country='United Kingdom', postcode=postcode, childcare_address=True, current_address=False, move_in_month=0, move_in_year=0, personal_detail_id=personal_detail_record)
        childcare_address_record.save()
            
    # If a record exists, update it
    elif Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id, childcare_address='True').count() > 0:
        
        # Retrieve the Your personal details record corresponding to the application
        childcare_address_record = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id, childcare_address=True)
        # Update the record
        childcare_address_record.street_line1 = street_line1
        childcare_address_record.street_line2 = street_line2
        childcare_address_record.town = town
        childcare_address_record.county = county
        childcare_address_record.postcode = postcode
        childcare_address_record.current_address = False
    
    return childcare_address_record


# Business logic to create or update a First aid training record
def First_Aid_Logic(application_id_local, form):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)

    # Get entered data to insert into the database
    training_organisation = form.cleaned_data.get('first_aid_training_organisation')
    course_title = form.cleaned_data.get('title_of_training_course')
    course_day = form.cleaned_data.get('course_date').day
    course_month = form.cleaned_data.get('course_date').month
    course_year = form.cleaned_data.get('course_date').year
    
    # If the user entered information for this task for the first time
    if First_Aid_Training.objects.filter(application_id=application_id_local).count() == 0:
                
        # Create a new First aid training record corresponding to the application
        first_aid_training_record = First_Aid_Training(training_organisation=training_organisation,course_title=course_title, course_day=course_day, course_month=course_month, course_year=course_year, application_id=this_application)
            
    # If a record exists, update it
    elif First_Aid_Training.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the First aid training record corresponding to the application      
        first_aid_training_record = First_Aid_Training.objects.get(application_id=application_id_local)
        # Return the record
        first_aid_training_record.training_organisation = training_organisation
        first_aid_training_record.course_title = course_title
        first_aid_training_record.course_day = course_day
        first_aid_training_record.course_month = course_month
        first_aid_training_record.course_year = course_year
    
    return first_aid_training_record


# Business logic to create or update a Your criminal record (DBS) check record
def dbs_check_logic(application_id_local, form):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into database
    dbs_certificate_number = form.cleaned_data.get('dbs_certificate_number')
    cautions_convictions = form.cleaned_data.get('convictions')
    
    # If the user entered information for this task for the first time
    if Criminal_Record_Check.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new Your criminal record (DBS) check record corresponding to the application
        dbs_record = Criminal_Record_Check(dbs_certificate_number=dbs_certificate_number, cautions_convictions=cautions_convictions, application_id=this_application)
    
    # If a record exists, update it
    elif Criminal_Record_Check.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the Your criminal record (DBS) check record corresponding to the application
        dbs_record = Criminal_Record_Check.objects.get(application_id=application_id_local)
        # Return the record
        dbs_record.dbs_certificate_number = dbs_certificate_number
        dbs_record.cautions_convictions = cautions_convictions
        
    return dbs_record


# Business logic to create or update a 2 references record                
def references_check_logic(application_id_local, form):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into database
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    relationship = form.cleaned_data.get('relationship')
    
    # If the user entered information for this task for the first time
    if References.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new 2 references record corresponding to the application
        reference_record = References(first_name=first_name,last_name=last_name,relationship=relationship,years_known=0,months_known=0,street_line1='',street_line2='',town='',county='',country='',postcode='',phone_number='',email='',application_id=this_application)
    
    # If a record exists, update it
    elif References.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the 2 references record corresponding to the application
        reference_record = References.objects.get(application_id=application_id_local)
        reference_record.first_name = first_name
        reference_record.last_name = last_name
        reference_record.relationship = relationship

    return reference_record


# Business logic to create or update a Your health record
def health_check_logic(application_id_local, form):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # Get entered data to insert into database
    movement_problems = form.cleaned_data.get('walking_bending')
    breathing_problems = form.cleaned_data.get('asthma_breathing')
    heart_disease = form.cleaned_data.get('heart_disease')
    blackout_epilepsy = form.cleaned_data.get('blackout_epilepsy')
    mental_health_problems = form.cleaned_data.get('mental_health')
    alcohol_drug_problems = form.cleaned_data.get('alcohol_drugs')
    
    # If no record exists, create a new one
    if Health_Declaration_Booklet.objects.filter(application_id=application_id_local).count() == 0:
        
        # Create a new Your health record corresponding to the application        
        hdb_record = Health_Declaration_Booklet(movement_problems=movement_problems, breathing_problems=breathing_problems, heart_disease=heart_disease, blackout_epilepsy=blackout_epilepsy, mental_health_problems=mental_health_problems, alcohol_drug_problems=alcohol_drug_problems, application_id=this_application)
      
    # If a record exists, update it
    elif Health_Declaration_Booklet.objects.filter(application_id=application_id_local).count() > 0:
        
        # Retrieve the Your health record corresponding to the application        
        hdb_record = Health_Declaration_Booklet.objects.get(application_id=application_id_local)
        hdb_record.movement_problems = movement_problems
        hdb_record.breathing_problems = breathing_problems
        hdb_record.heart_disease = heart_disease
        hdb_record.blackout_epilepsy = blackout_epilepsy
        hdb_record.mental_health_problems = mental_health_problems
        hdb_record.alcohol_drug_problems = alcohol_drug_problems

    return hdb_record

def get_card_expiry_years():
    
    # Output list
    year_list = []
    
    # Iterates 0 through 10, affixing each value to current year and appending to yearlist
    for year_iterable in range(0,11):
        
        now = datetime.datetime.now()
        year_list.append((now.year+year_iterable,(str(now.year+year_iterable))))
        
    return year_list