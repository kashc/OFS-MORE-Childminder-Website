"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Business Logic Unit Tests --

@author: Informed Solutions
"""


import datetime

from datetime import date
from django.test import TestCase
from uuid import UUID

from .models import (Application, ApplicantName, ApplicantPersonalDetails, ChildcareType,
                     CriminalRecordCheck, FirstAidTraining, HealthDeclarationBooklet, UserDetails,
                     Reference, ApplicantHomeAddress)


# Test business logic to create or update a Type of childcare record
class Test_ChildcareType_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test ChildcareType object if it already exists
        ChildcareType.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the ChildcareType object corresponding with the test application does not exist
        assert(ChildcareType.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application and login IDs
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
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
        
        # Create a test childcare ID
        test_childcare_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test ChildcareType object
        ChildcareType.objects.create(
            childcare_id = (UUID(test_childcare_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            zero_to_five = 'True',
            five_to_eight = 'False',
            eight_plus = 'True'
        )
        
        # Verify that the ChildcareType object corresponding with the test application exists
        assert(ChildcareType.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        ChildcareType.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


# Test business logic to create or update a Your Personal Details record
class Test_Personal_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_dob_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application do not exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_dob_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() > 0)
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_name_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantName.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application do not exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() == 0)
        assert(ApplicantName.objects.filter(personal_detail_id=test_personal_detail_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_name_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantName.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test name ID
        test_name_id = '6e09fe41-2b07-4177-a5e4-347b2515ea8e'
        
        # Create a test Applicant_Names object
        ApplicantName.objects.create(
            name_id = (UUID(test_name_id)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            current_name = 'True',
            first_name = 'Erik',
            middle_names = 'Tolstrup',
            last_name = 'Odense'
        )
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() > 0)
        assert(ApplicantName.objects.filter(personal_detail_id=test_personal_detail_id).count() > 0)
 
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_home_address_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Create a test home address ID
        test_home_address_id = '11a3aef5-9e23-4216-b646-e6adccda4270'
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(home_address_id=test_home_address_id, current_address=True).delete()
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application do not exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() == 0)
        assert(ApplicantHomeAddress.objects.filter(home_address_id=test_home_address_id, current_address=True).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_home_address_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test address ID
        test_home_address_id = '11a3aef5-9e23-4216-b646-e6adccda4270'
        
        # Create a test Applicant_Home_Address object
        ApplicantHomeAddress.objects.create(
            home_address_id = (UUID(test_home_address_id)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            childcare_address = None,
            current_address = True,
            move_in_month = 0,
            move_in_year = 0
        )
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() > 0)
        assert(ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id, current_address=True).count() > 0)

    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_childcare_address_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test address ID
        test_home_address_id = '11a3aef5-9e23-4216-b646-e6adccda4270'
        
        # Create a test Applicant_Home_Address object
        ApplicantHomeAddress.objects.create(
            home_address_id = (UUID(test_home_address_id)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            childcare_address = False,
            current_address = True,
            move_in_month = 0,
            move_in_year = 0
        )
        
        # Delete test Applicant_Personal_Details and Applicant_Names objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(home_address_id=test_home_address_id, childcare_address=True).delete()
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application do not exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() == 0)
        assert(ApplicantHomeAddress.objects.filter(home_address_id=test_home_address_id, childcare_address=True).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_childcare_address_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test address ID
        test_home_address_id = '11a3aef5-9e23-4216-b646-e6adccda4270'
        
        # Create a test Applicant_Home_Address object
        ApplicantHomeAddress.objects.create(
            home_address_id = (UUID(test_home_address_id)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            childcare_address = True,
            current_address = False,
            move_in_month = 0,
            move_in_year = 0
        )
        
        # Verify that the Applicant_Personal_Details and Applicant_Names objects corresponding with the test application exist
        assert(ApplicantPersonalDetails.objects.filter(application_id=test_application_id).count() > 0)
        assert(ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id, childcare_address=True).count() > 0)
    
    # Test logic to remove multiple childcare addresses
    def test_multiple_childcare_address_logic(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test personal detail ID
        test_personal_detail_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Applicant_Personal_Details, Applicant_Names and UserDetails objects if they already exist
        ApplicantPersonalDetails.objects.filter(application_id=test_application_id).delete()
        ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test Applicant_Personal_Details object
        ApplicantPersonalDetails.objects.create(
            personal_detail_id = (UUID(test_personal_detail_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            birth_day = '00',
            birth_month = '00',
            birth_year = '0000'
        )
        
        # Create a test address ID
        test_home_address_id = '11a3aef5-9e23-4216-b646-e6adccda4270'
        
        # Create a test Applicant_Home_Address object
        ApplicantHomeAddress.objects.create(
            home_address_id = (UUID(test_home_address_id)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            childcare_address = True,
            current_address = False,
            move_in_month = 0,
            move_in_year = 0
        )

        # Create another test address ID
        test_home_address_id2 = 'd51b854d-30b0-4889-88d4-804b2c6215e4'
        
        # Create a another test Applicant_Home_Address object
        ApplicantHomeAddress.objects.create(
            home_address_id = (UUID(test_home_address_id2)),
            personal_detail_id = ApplicantPersonalDetails.objects.get(personal_detail_id=test_personal_detail_id),
            street_line1 = '',
            street_line2 = '',
            town = '',
            county = '',
            country = '',
            postcode = '',
            childcare_address = True,
            current_address = True,
            move_in_month = 0,
            move_in_year = 0
        )        
        
        assert(ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id, childcare_address=True).count() > 1)
        assert(ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id, childcare_address=True, current_address=True).count() > 0)
        assert(ApplicantHomeAddress.objects.filter(personal_detail_id=test_personal_detail_id, childcare_address=True, current_address=False).count() > 0)

    # Delete test application
    def delete(self):
        
        ApplicantHomeAddress.objects.filter(name_id='11a3aef5-9e23-4216-b646-e6adccda4270').delete()
        ApplicantPersonalDetails.objects.filter(personal_detail_id='166f77f7-c2ee-4550-9461-45b9d2f28d34').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


# Test business logic to create or update a First aid training record
class Test_First_Aid_Training_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test First_Aid_Training object if it already exists
        FirstAidTraining.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the First_Aid_Training object corresponding with the test application does not exist
        assert(FirstAidTraining.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test First_Aid_Training and UserDetails objects if they already exist
        FirstAidTraining.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test first aid ID
        test_first_aid_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test First_Aid_Training object
        FirstAidTraining.objects.create(
            first_aid_id = (UUID(test_first_aid_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            training_organisation = 'Red Cross',
            course_title = 'Infant First Aid',
            course_day = '01',
            course_month = '02',
            course_year = '2003'
        )
        
        # Verify that the First_Aid_Training object corresponding with the test application exists
        assert(FirstAidTraining.objects.filter(application_id=test_application_id).count() > 0)
    
    # Test logic to go to declaration page
    def test_logic_to_go_to_declaration(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test First_Aid_Training and UserDetails objects if they already exist
        FirstAidTraining.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'NOT_STARTED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test first aid ID
        test_first_aid_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test First_Aid_Training object
        test_first_aid = FirstAidTraining.objects.create(
            first_aid_id = (UUID(test_first_aid_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            training_organisation = 'Red Cross',
            course_title = 'Infant First Aid',
            course_day = 1,
            course_month = 2,
            course_year = 2017
        )
        
        test_date = date(2018, 1, 5)
        
        certificate_day = test_first_aid.course_day
        certificate_month = test_first_aid.course_month
        certificate_year = test_first_aid.course_year
        certificate_date = date(certificate_year, certificate_month, certificate_day)
            
        # Calculate certificate age
        certificate_age = test_date.year - certificate_date.year - ((test_date.month, test_date.day) < (certificate_date.month, certificate_date.day))
        
        assert(certificate_age < 2.5)
        
    # Test logic to go to renew page
    def test_logic_to_go_to_renew(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test First_Aid_Training and UserDetails objects if they already exist
        FirstAidTraining.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'NOT_STARTED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test first aid ID
        test_first_aid_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test First_Aid_Training object
        test_first_aid = FirstAidTraining.objects.create(
            first_aid_id = (UUID(test_first_aid_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            training_organisation = 'Red Cross',
            course_title = 'Infant First Aid',
            course_day = 1,
            course_month = 2,
            course_year = 2014
        )
        
        test_date = date(2018, 1, 5)
        
        certificate_day = test_first_aid.course_day
        certificate_month = test_first_aid.course_month
        certificate_year = test_first_aid.course_year
        certificate_date = date(certificate_year, certificate_month, certificate_day)
            
        # Calculate certificate age
        certificate_age = test_date.year - certificate_date.year - ((test_date.month, test_date.day) < (certificate_date.month, certificate_date.day))
        
        assert(2.5 <= certificate_age <= 3)     

    # Test logic to go to training page
    def test_logic_to_go_to_training(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test First_Aid_Training and UserDetails objects if they already exist
        FirstAidTraining.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'NOT_STARTED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test first aid ID
        test_first_aid_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test First_Aid_Training object
        test_first_aid = FirstAidTraining.objects.create(
            first_aid_id = (UUID(test_first_aid_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            training_organisation = 'Red Cross',
            course_title = 'Infant First Aid',
            course_day = 1,
            course_month = 2,
            course_year = 1995
        )
        
        test_date = date(2018, 1, 5)
        
        certificate_day = test_first_aid.course_day
        certificate_month = test_first_aid.course_month
        certificate_year = test_first_aid.course_year
        certificate_date = date(certificate_year, certificate_month, certificate_day)
            
        # Calculate certificate age
        certificate_age = test_date.year - certificate_date.year - ((test_date.month, test_date.day) < (certificate_date.month, certificate_date.day))
        
        assert(certificate_age > 3)
           
    # Delete test application
    def delete(self):
        
        FirstAidTraining.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


# Test business logic to create or update a Your criminal record (DBS) check record
class Test_DBS_Check_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Criminal_Record_Check object if it already exists
        CriminalRecordCheck.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Criminal_Record_Check object corresponding with the test application does not exist
        assert(CriminalRecordCheck.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Criminal_Record_Check and UserDetails objects if they already exist
        CriminalRecordCheck.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test criminal record ID
        test_criminal_record_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Criminal_Record_Check object
        CriminalRecordCheck.objects.create(
            criminal_record_id = (UUID(test_criminal_record_id)),
            application_id = Application.objects.get(application_id=test_application_id),
            dbs_certificate_number = '123456789012',
            cautions_convictions = 'True'
        )
        
        # Verify that the Criminal_Record_Check object corresponding with the test application exists
        assert(CriminalRecordCheck.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        CriminalRecordCheck.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()
        

# Test business logic to create or update a Your health record
class Test_Health_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test Health_Declaration_Booklet object if it already exists
        HealthDeclarationBooklet.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the Health_Declaration_Booklet object corresponding with the test application does not exist
        assert(HealthDeclarationBooklet.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test Health_Declaration_Booklet and UserDetails objects if they already exist
        HealthDeclarationBooklet.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test HDB ID
        test_hdb_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test Health_Declaration_Booklet object
        HealthDeclarationBooklet.objects.create(
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
        assert(HealthDeclarationBooklet.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        HealthDeclarationBooklet.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


# Test business logic to create or update a 2 references record
class Test_References_Logic(TestCase):
    
    # Test the business case where a new record needs to be created
    def test_logic_to_create_new_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        
        # Delete test References object if it already exists
        Reference.objects.filter(application_id=test_application_id).delete()
        
        # Verify that the References object corresponding with the test application does not exist
        assert(Reference.objects.filter(application_id=test_application_id).count() == 0)
    
    # Test the business case where a record already exists
    def test_logic_to_update_record(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'

        # Create a test login ID
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        
        # Delete test References and UserDetails objects if they already exist
        Reference.objects.filter(application_id=test_application_id).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        
        # Create a test user
        user = UserDetails.objects.create(
            login_id = (UUID(test_login_id)),
            email = '',
            mobile_number = '',
            add_phone_number = '',
            email_expiry_date = None,
            sms_expiry_date = None,
            magic_link_email = '',
            magic_link_sms = ''
        )
        
        # Create a test application
        Application.objects.create(
            application_id = (UUID(test_application_id)),
            login_id = user,
            application_type = 'CHILDMINDER',
            application_status = 'DRAFTING',
            cygnum_urn = '',   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
            date_created = datetime.datetime.today(),
            date_updated = datetime.datetime.today(),
            date_accepted = None
        )
        
        # Create a test reference ID
        test_reference_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        
        # Create a test References object
        Reference.objects.create(
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
        assert(Reference.objects.filter(application_id=test_application_id).count() > 0)
    
    # Delete test application
    def delete(self):
        
        Reference.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        Application.objects.filter(application_id='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()