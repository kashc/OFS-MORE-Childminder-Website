'''
Created on 18 Dec 2017

OFS-MORE: Apply to be a Childminder Beta

@author: Informed Solutions
'''

from django.test import Client
from django.test import TestCase
from django.urls import resolve

from .models import Application, Childcare_Type, Login_And_Contact_Details

from uuid import UUID


# Test business logic to create or update a Type of childcare record
class Test_Childcare_Type_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Childcare_Type object if it already exists
        Childcare_Type.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Childcare_Type object corresponding with the test application does not exist
        assert(Childcare_Type.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Childcare_Type object if it already exists
        Childcare_Type.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID('f8c42666-1367-4878-92e2-1cee6ebcb48c')),   
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
        )
        
        # Create a test childcare ID
        test_childcare_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Childcare_Type object
        Childcare_Type.objects.create(
            childcare_id = (UUID(test_childcare_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            zero_to_five = 'True',
            five_to_eight = 'False',
            eight_plus = 'True'
        )
        
        # Verify that the Childcare_Type object corresponding with the test application exists
        assert(Childcare_Type.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Childcare_Type.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a Your Login and Contact Details record
class Test_Login_Contact_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Login_And_Contact_Details object if it already exists
        Login_And_Contact_Details.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Login_And_Contact_Details object corresponding with the test application does not exist
        assert(Login_And_Contact_Details.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Login_And_Contact_Details object if it already exists
        Login_And_Contact_Details.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID('f8c42666-1367-4878-92e2-1cee6ebcb48c')),   
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
        )
        
        # Create a test login ID
        test_login_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Login_And_Contact_Details object
        Login_And_Contact_Details.objects.create(
            login_id = (UUID(test_login_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            email = 'test@gmail.com',
            mobile_number = '',
            add_phone_number = ''
        )
        
        # Verify that the Login_And_Contact_Detilas object corresponding with the test application exists
        assert(Login_And_Contact_Details.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Login_And_Contact_Details.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()