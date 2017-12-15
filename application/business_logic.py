'''
Created on 15 Dec 2017

OFS-MORE: Apply to be a Childminder Beta

@author: Informed Solutions
'''

from .models import Application, Childcare_Type, Login_And_Contact_Details


# Business logic to create or update a Type of childcare record
def Childcare_Type_Logic(application_id_local, zero_to_five_status, five_to_eight_status, eight_plus_status):
    
    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)
    
    # If the user entered information for this task for the first time
    if Childcare_Type.objects.filter(application_id=application_id_local).count() == 0:
                
        # Create a new Type of childcare record with the entered data
        childcare_type_record = Childcare_Type(zero_to_five=zero_to_five_status, five_to_eight=five_to_eight_status, eight_plus=eight_plus_status, application_id=this_application)
            
    # If the user previously entered information for this task
    elif Childcare_Type.objects.filter(application_id=application_id_local).count() > 0:
            
        # Retrieve the Type of childcare record corresponding to the application
        childcare_type_record = Childcare_Type.objects.get(application_id=application_id_local)
        # Update the record
        childcare_type_record.zero_to_five = zero_to_five_status
        childcare_type_record.five_to_eight = five_to_eight_status
        childcare_type_record.eight_plus = eight_plus_status
    
    return childcare_type_record


# Business logic to create or update a Your login and contact details record
def Login_Contact_Logic(application_id_local, email_address):

    # Retrieve the application's ID
    this_application = Application.objects.get(application_id=application_id_local)

    # If the user entered information for this task for the first time
    if Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() == 0:
            
        # Create a new Your login and contact details record corresponding to the application
        login_and_contact_details_record = Login_And_Contact_Details(email=email_address, application_id=this_application)
            
    # If the user previously entered information for this task
    elif Login_And_Contact_Details.objects.filter(application_id=application_id_local).count() > 0:
                
        # Retrieve the Your login and contact details record corresponding to the application
        login_and_contact_details_record = Login_And_Contact_Details.objects.get(application_id=application_id_local)
        # Update the record
        login_and_contact_details_record.email = email_address

    return login_and_contact_details_record