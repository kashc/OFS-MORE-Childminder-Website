'''
Created on 15 Dec 2017

@author: Informed Solutions
'''

from application.models import Application, Childcare_Type, Login_And_Contact_Details, Applicant_Personal_Details, Applicant_Names, Applicant_Home_Address, Criminal_Record_Check, Adults_In_Home, Children_In_Home

from django.test import TestCase

from uuid import UUID


class ApplicantTestCase (TestCase):

    # Set up a test application
    def setUp(self):
        
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
    
    # Remove the test application   
    def tearDown(self):
        
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()    
    
    # Test that an application can be correctly created    
    def test_application_can_be_created(self):
        
        application = Application.objects.get(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c')
        
        application_statuses = dict({
            'application_id': application.application_id,
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
        })
        
        assert(application_statuses=={'application_id': UUID('f8c42666-1367-4878-92e2-1cee6ebcb48c'), 'login_details_status': 'NOT_STARTED', 'personal_details_status': 'NOT_STARTED', 'childcare_type_status': 'NOT_STARTED', 'first_aid_training_status': 'NOT_STARTED', 'eyfs_training_status': 'NOT_STARTED', 'criminal_record_check_status': 'NOT_STARTED', 'health_status': 'NOT_STARTED', 'reference_status': 'NOT_STARTED', 'people_in_home_status': 'NOT_STARTED', 'declaration_status': 'NOT_STARTED'})
    
    # Test that an application can be correctly updated
    def test_application_can_be_updated(self):
        
        application = Application.objects.get(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c')
        application.login_details_status = 'IN_PROGRESS'
        application.childcare_type_status = 'COMPLETED'
        application.save()
        
        application_statuses = dict({
            'application_id': application.application_id,
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
        }) 
        
        assert(application_statuses=={'application_id': UUID('f8c42666-1367-4878-92e2-1cee6ebcb48c'), 'login_details_status': 'IN_PROGRESS', 'personal_details_status': 'NOT_STARTED', 'childcare_type_status': 'COMPLETED', 'first_aid_training_status': 'NOT_STARTED', 'eyfs_training_status': 'NOT_STARTED', 'criminal_record_check_status': 'NOT_STARTED', 'health_status': 'NOT_STARTED', 'reference_status': 'NOT_STARTED', 'people_in_home_status': 'NOT_STARTED', 'declaration_status': 'NOT_STARTED'})