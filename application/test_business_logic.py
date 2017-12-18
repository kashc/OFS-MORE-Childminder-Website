'''
Created on 18 Dec 2017

OFS-MORE: Apply to be a Childminder Beta

@author: Informed Solutions
'''

from django.test import Client
from django.test import TestCase
from django.urls import resolve

from .models import Application, Applicant_Names, Applicant_Personal_Details, Childcare_Type, Criminal_Record_Check, First_Aid_Training, Health_Declaration_Booklet, Login_And_Contact_Details, References

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
        Childcare_Type.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        Login_And_Contact_Details.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Verify that the Login_And_Contact_Details object corresponding with the test application exists
        assert(Login_And_Contact_Details.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Login_And_Contact_Details.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a Your Personal Details record
class Test_Personal_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        Applicant_Personal_Details.objects.filter(application_id=test_application_id).delete()
        Applicant_Names.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application do not exist
        assert(Applicant_Personal_Details.objects.filter(application_id=test_application_id).count() == 0)
        assert(Applicant_Names.objects.filter(personal_detail_id=test_personal_detail_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        Applicant_Personal_Details.objects.filter(application_id=test_application_id).delete()
        Applicant_Names.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Create a test Applicant_Personal_Details object
        Applicant_Personal_Details.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test name ID
        test_name_id = '6e09fe41-2b07-4177-a5e4-347b2515ea8e'
        
        # Create a test Applicant_Names object
        Applicant_Names.objects.create(
            name_id = (UUID(test_name_id)),
            personal_detail_id = Applicant_Personal_Details.objects.get(personal_detail_id=test_personal_detail_id),
            current_name = 'True',
            first_name = 'Erik',
            middle_names = 'Tolstrup',
            last_name = 'Odense'
        )
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application exist
        assert(Applicant_Personal_Details.objects.filter(application_id=test_application_id).count() > 0)
        assert(Applicant_Names.objects.filter(personal_detail_id=test_personal_detail_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Applicant_Names_Details.objects.filter(name_id='6e09fe41-2b07-4177-a5e4-347b2515ea8e').delete()
        Applicant_Personal_Details.objects.filter(personal_detail_id='166f77f7-c2ee-4550-9461-45b9d2f28d34').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a First aid training record
class Test_First_Aid_Training_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test First_Aid_Training object if it already exists
        First_Aid_Training.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the First_Aid_Training object corresponding with the test application does not exist
        assert(First_Aid_Training.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test First_Aid_Training object if it already exists
        First_Aid_Training.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Create a test first aid ID
        test_first_aid_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test First_Aid_Training object
        First_Aid_Training.objects.create(
            first_aid_id = (UUID(test_first_aid_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            training_organisation = 'Red Cross',
            course_title = 'Infant First Aid',
            course_day = '01',
            course_month = '02',
            course_year = '2003'
        )
        
        # Verify that the First_Aid_Training object corresponding with the test application exists
        assert(First_Aid_Training.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        First_Aid_Training.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a Your criminal record (DBS) check record
class Test_DBS_Check_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Criminal_Record_Check object if it already exists
        Criminal_Record_Check.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Criminal_Record_Check object corresponding with the test application does not exist
        assert(Criminal_Record_Check.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Criminal_Record_Check object if it already exists
        Criminal_Record_Check.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Create a test criminal record ID
        test_criminal_record_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Criminal_Record_Check object
        Criminal_Record_Check.objects.create(
            criminal_record_id = (UUID(test_criminal_record_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            dbs_certificate_number = '123456789012',
            cautions_convictions = 'True'
        )
        
        # Verify that the Criminal_Record_Check object corresponding with the test application exists
        assert(Criminal_Record_Check.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Criminal_Record_Check.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a Your health record
class Test_Health_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Health_Declaration_Booklet object if it already exists
        Health_Declaration_Booklet.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Health_Declaration_Booklet object corresponding with the test application does not exist
        assert(Health_Declaration_Booklet.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Health_Declaration_Booklet object if it already exists
        Health_Declaration_Booklet.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Create a test HDB ID
        test_hdb_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Health_Declaration_Booklet object
        Health_Declaration_Booklet.objects.create(
            hdb_id = (UUID(test_hdb_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            movement_problems = 'True',
            breathing_problems = 'True',
            heart_disease = 'True',
            blackout_epilepsy = 'True',
            mental_health_problems = 'True',
            alcohol_drug_problems = 'True',
            health_details = ''
        )
        
        # Verify that the Health_Declaration_Booklet object corresponding with the test application exists
        assert(Health_Declaration_Booklet.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Health_Declaration_Booklet.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test business logic to create or update a 2 references record
class Test_References_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test References object if it already exists
        References.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the References object corresponding with the test application does not exist
        assert(References.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test References object if it already exists
        References.objects.filter(application_id=test_application_id).delete()
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),   
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
        
        # Create a test reference ID
        test_reference_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test References object
        References.objects.create(
            reference_id = (UUID(test_reference_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            first_name = 'Hugo',
            last_name = 'Geeves',
            relationship = 'Colleague',
            years_known = '00',
            months_known = '00',
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            phone_number = '',
            email = ''
        )
        
        # Verify that the References object corresponding with the test application exists
        assert(References.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        References.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()