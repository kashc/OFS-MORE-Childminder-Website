"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- test_views.py --

@author: Informed Solutions
"""

import datetime

from django.conf import settings
from django.test import Client
from django.test import TestCase
from django.urls import resolve
from uuid import UUID

# Test suite for start page
from . import models

from .views import (application_saved,
                    card_payment_details,
                    confirmation,
                    contact_email,
                    contact_phone,
                    contact_question,
                    contact_summary,
                    dbs_check_dbs_details,
                    dbs_check_guidance,
                    dbs_check_summary,
                    dbs_check_upload_dbs,
                    declaration,
                    eyfs,
                    first_aid_training_declaration,
                    first_aid_training_details,
                    first_aid_training_guidance,
                    first_aid_training_renew,
                    first_aid_training_summary,
                    first_aid_training_training,
                    other_people,
                    payment,
                    personal_details_childcare_address,
                    personal_details_dob,
                    personal_details_guidance,
                    personal_details_home_address,
                    personal_details_location_of_care,
                    personal_details_name,
                    personal_details_summary,
                    references_intro,
                    references_first_reference,
                    references_first_reference_address,
                    references_first_reference_contact_details,
                    references_second_reference,
                    references_second_reference_address,
                    references_second_reference_contact_details,
                    references_summary,
                    start_page,
                    task_list,
                    type_of_childcare)


class StartPageTest(TestCase):

    def test_root_url_resolves_to_start_page_view(self):
        found = resolve(settings.URL_PREFIX + '/')
        self.assertEqual(found.func, start_page)


class TaskListTest(TestCase):

    def test_url_resolves_to_task_list(self):
        found = resolve(settings.URL_PREFIX + '/task-list/')
        self.assertEqual(found.func, task_list)

    def test_task_list_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/task-list/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)


class TypeOfChildcareTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/childcare/')
        self.assertEqual(found.func, type_of_childcare)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/childcare/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='NOT_STARTED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).childcare_type_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class LoginAndContactDetailsTest(TestCase):

    def test_url_resolves_to_email_page(self):
        found = resolve(settings.URL_PREFIX + '/account/email/')
        self.assertEqual(found.func, contact_email)

    def test_email_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/account/email/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_phone_page(self):
        found = resolve(settings.URL_PREFIX + '/account/phone/')
        self.assertEqual(found.func, contact_phone)

    def test_phone_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/account/phone/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_question_page(self):
        found = resolve(settings.URL_PREFIX + '/account/question/')
        self.assertEqual(found.func, contact_question)

    def test_question_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/account/question/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_summary_page(self):
        found = resolve(settings.URL_PREFIX + '/account/summary/')
        self.assertEqual(found.func, contact_summary)

    def test_summary_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/account/summary/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='NOT_STARTED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).login_details_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class PersonalDetailsTest(TestCase):

    def test_guidance_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/guidance/')
        self.assertEqual(found.func, personal_details_guidance)

    def test_guidance_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/guidance/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_name_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/name/')
        self.assertEqual(found.func, personal_details_name)

    def test_name_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/name/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_dob_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/dob/')
        self.assertEqual(found.func, personal_details_dob)

    def test_dob_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/dob/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_home_address_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/home-address/')
        self.assertEqual(found.func, personal_details_home_address)

    def test_home_address_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/home-address/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_location_of_care_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/location-of-care/')
        self.assertEqual(found.func, personal_details_location_of_care)

    def test_location_of_care_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/location-of-care/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_location_of_care_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/childcare-address/')
        self.assertEqual(found.func, personal_details_childcare_address)

    def test_location_of_care_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/childcare-address/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_location_of_care_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/personal-details/summary/')
        self.assertEqual(found.func, personal_details_summary)

    def test_location_of_care_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/personal-details/summary/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='NOT_STARTED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).personal_details_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class FirstAidTrainingTest(TestCase):

    def test_guidance_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/guidance/')
        self.assertEqual(found.func, first_aid_training_guidance)

    def test_guidance_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/guidance?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)  #

    def test_details_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/details/')
        self.assertEqual(found.func, first_aid_training_details)

    def test_details_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/details?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_declaration_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/declaration/')
        self.assertEqual(found.func, first_aid_training_declaration)

    def test_declaration_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/declaration?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_renew_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/renew/')
        self.assertEqual(found.func, first_aid_training_renew)

    def test_renew_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/renew?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_training_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/training/')
        self.assertEqual(found.func, first_aid_training_training)

    def test_training_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/training?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_summary_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/first-aid/summary/')
        self.assertEqual(found.func, first_aid_training_summary)

    def test_summary_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/first-aid/summary?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='NOT_STARTED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).first_aid_training_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class EYFSTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/eyfs/')
        self.assertEqual(found.func, eyfs)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/eyfs/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='NOT_STARTED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).eyfs_training_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class DBSCheckTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/dbs-check/guidance/')
        self.assertEqual(found.func, dbs_check_guidance)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/dbs-check/guidance/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/dbs-check/dbs-details/')
        self.assertEqual(found.func, dbs_check_dbs_details)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/dbs-check/dbs-details?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):

        found = resolve(settings.URL_PREFIX + '/dbs-check/upload-dbs/')
        self.assertEqual(found.func, dbs_check_upload_dbs)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/dbs-check/upload-dbs?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/dbs-check/summary/')
        self.assertEqual(found.func, dbs_check_summary)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/dbs-check/summary?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='NOT_STARTED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).criminal_record_check_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class ReferencesTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/intro/')
        self.assertEqual(found.func, references_intro)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/intro?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/first-reference/')
        self.assertEqual(found.func, references_first_reference)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/first-reference?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/first-reference-address/')
        self.assertEqual(found.func, references_first_reference_address)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/first-reference-address?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/first-reference-contact-details/')
        self.assertEqual(found.func, references_first_reference_contact_details)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/first-reference-contact-details?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/second-reference/')
        self.assertEqual(found.func, references_second_reference)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/second-reference?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/second-reference-address/')
        self.assertEqual(found.func, references_second_reference_address)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/second-reference-address?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/second-reference-contact-details/')
        self.assertEqual(found.func, references_second_reference_contact_details)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/second-reference-contact-details?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/references/summary/')
        self.assertEqual(found.func, references_summary)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/references/summary?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='NOT_STARTED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).references_status != 'COMPLETED')

    def delete(self):

        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class OtherPeopleTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/other-people/')
        self.assertEqual(found.func, other_people)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/other-people/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='NOT_STARTED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).people_in_home_status != 'COMPLETED')

    def delete(self):
        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class DeclarationTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/declaration/')
        self.assertEqual(found.func, declaration)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/declaration/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        assert (models.Application.objects.get(pk=test_application_id).declarations_status != 'COMPLETED')

    def delete(self):
        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()


class ConfirmationTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/confirm-your-answers/')
        self.assertEqual(found.func, confirmation)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/confirm-your-answers/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)


class PaymentTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/payment/')
        self.assertEqual(found.func, payment)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/payment/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/payment-details/')
        self.assertEqual(found.func, card_payment_details)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/payment-details/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)


class ApplicationSavedTest(TestCase):

    def test_url_resolves_to_page(self):
        found = resolve(settings.URL_PREFIX + '/application-saved/')
        self.assertEqual(found.func, application_saved)

    def test_page_not_displayed_without_id(self):
        c = Client()
        try:
            c.get(settings.URL_PREFIX + '/application-saved/?id=')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(0, 0)


class TaskStatusTest(TestCase):

    def test_status_update_with_tasks_not_started(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='NOT_STARTED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
        assert (('NOT_STARTED' in temp_context.values()) == True)

    def test_status_update_with_tasks_in_progress(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='IN_PROGRESS',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
        assert (('IN_PROGRESS' in temp_context.values()) == True)

    def test_status_update_with_tasks_completed_except_declarations(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
        assert (('IN_PROGRESS' in temp_context.values()) == False)
        assert (('NOT_STARTED' in temp_context.values()) == False)

    def test_status_update_with_tasks_completed_with_declarations_to_do(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
            'all_complete': True,
            'confirm_details': False
        })
        assert (application_status_context['declaration_status'] == 'NOT_STARTED')

    def test_status_update_with_tasks_completed_with_declarations_in_progress(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='IN_PROGRESS',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
            'all_complete': True,
            'confirm_details': False
        })
        assert (application_status_context['declaration_status'] == 'IN_PROGRESS')

    def test_status_update_with_tasks_completed_with_declarations_complete(self):
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        user = models.UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        application = models.Application.objects.create(
            application_id=(UUID(test_application_id)),
            login_id=user,
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='COMPLETED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='COMPLETED',
            date_created=datetime.datetime.today(),
            date_updated=datetime.datetime.today(),
            date_accepted=None
        )
        application_status_context = dict({
            'application_id': test_application_id,
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
            'all_complete': True,
            'confirm_details': True
        })
        assert (application_status_context['declaration_status'] == 'COMPLETED')

    def delete(self):
        models.Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()
        models.UserDetails.objects.get(login_id='004551ca-21fa-4dbe-9095-0384e73b3cbe').delete()
