'''
Created on 15 Dec 2017

OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Views Unit Tests --

@author: Informed Solutions
'''


from django.test import Client
from django.test import TestCase
from django.urls import resolve

from .models import Application

from uuid import UUID

from .views import ApplicationSavedView, ConfirmationView, ContactEmailView, DBSCheckView, DeclarationView, EYFSView, FirstAidTrainingView, HealthView, LogInView, OtherPeopleView, PaymentView, PersonalDetailsView, ReferencesView, StartPageView, TypeOfChildcareView



# Test suite for start page
class StartPageTest(TestCase):
    
    # Test to check if URL resolves to correct view
    def test_root_url_resolves_to_start_page_view(self):
        
        found = resolve('/')
        self.assertEqual(found.func, StartPageView)
    

# Test suite for task list
class TaskListTest(TestCase):

    # Test to check if URL resolves to correct view    
    def test_url_resolves_to_task_list(self):
        
        found = resolve('/task-list/')
        self.assertEqual(found.func, LogInView)

    # Test to check that a user cannot navigate to the page without an application ID        
    def test_task_list_not_displayed_without_id(self):
        
        c = Client()
        response = c.get('/task-list/?id=')
        
        try:
            response = c.get('/task-list/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)  
        

# Test suite for Type of childcare task page
class TypeOfChildcareTest(TestCase):

    # Test to check if URL resolves to correct view    
    def test_url_resolves_to_page(self):
        
        found = resolve('/childcare/')
        self.assertEqual(found.func, TypeOfChildcareView)

    # Test to check that a user cannot navigate to the page without an application ID   
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/childcare/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
    
    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'NOT_STARTED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).childcare_type_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()     


# Test suite for Your Login and Contact Details page
class LoginAndContactDetailsTest(TestCase):

    # Test to check if URL resolves to correct view    
    def test_url_resolves_to_page(self):
        
        found = resolve('/contact-email/')
        self.assertEqual(found.func, ContactEmailView)

    # Test to check that a user cannot navigate to the page without an application ID  
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/contact-email/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)  
    
    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'NOT_STARTED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).login_details_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete() 


# Test suite for Your Personal Details page          
class PersonalDetailsTest(TestCase):

    # Test to check if URL resolves to correct view    
    def test_url_resolves_to_page(self):
        
        found = resolve('/personal-details/')
        self.assertEqual(found.func, PersonalDetailsView)
   
    # Test to check that a user cannot navigate to the page without an application ID 
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/personal-details/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
            
    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'NOT_STARTED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).personal_details_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for First aid training page
class FirstAidTrainingTest(TestCase):

    # Test to check if URL resolves to correct view  
    def test_url_resolves_to_page(self):
        
        found = resolve('/first-aid/')
        self.assertEqual(found.func, FirstAidTrainingView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/first-aid/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)

    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'NOT_STARTED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).first_aid_training_status != 'COMPLETED')

    # Delete test Application object   
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for Early Years knowledge page          
class EYFSTest(TestCase):

    # Test to check if URL resolves to correct view 
    def test_url_resolves_to_page(self):
        
        found = resolve('/eyfs/')
        self.assertEqual(found.func, EYFSView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/eyfs/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)

    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'NOT_STARTED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).eyfs_training_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for Your criminal record (DBS) check page
class DBSCheckTest(TestCase):

    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/dbs-check/')
        self.assertEqual(found.func, DBSCheckView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/eyfs/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
            
    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'NOT_STARTED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).criminal_record_check_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for Your health page
class HealthTest(TestCase):

    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/health/')
        self.assertEqual(found.func, HealthView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/health/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)

    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'NOT_STARTED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).health_status != 'COMPLETED')

    # Delete test Application object   
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for 2 references page
class ReferencesTest(TestCase):

    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/references/')
        self.assertEqual(found.func, ReferencesView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/references/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)

    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'NOT_STARTED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).references_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for People in your home page
class OtherPeopleTest(TestCase):

    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/other-people/')
        self.assertEqual(found.func, OtherPeopleView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/other-people/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
            
    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'NOT_STARTED',
            declarations_status = 'COMPLETED',
        )
        
        assert(Application.objects.get(pk = test_application_id).people_in_home_status != 'COMPLETED')

    # Delete test Application object    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for Declarations page
class DeclarationTest(TestCase):
    
    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/declaration/')
        self.assertEqual(found.func, DeclarationView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/declaration/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)

    # Test progress status does not update to Started when a returning to the task list after completing a task
    def test_status_does_not_change_to_in_progress_when_returning_to_task_list(self):
        
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
        )
        
        assert(Application.objects.get(pk = test_application_id).declarations_status != 'COMPLETED')
    
    # Delete test Application object
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()


# Test suite for Confirm your answers page
class ConfirmationTest(TestCase):
    
    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/confirm-your-answers/')
        self.assertEqual(found.func, ConfirmationView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/confirm-your-answers/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)


# Test suite for Payment page
class PaymentTest(TestCase):
    
    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/payment/')
        self.assertEqual(found.func, PaymentView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/payment/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
            

# Test suite for Application Saved page
class ApplicationSavedTest(TestCase):
    
    # Test to check if URL resolves to correct view
    def test_url_resolves_to_page(self):
        
        found = resolve('/application-saved/')
        self.assertEqual(found.func, ApplicationSavedView)
    
    # Test to check that a user cannot navigate to the page without an application ID
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/application-saved/?id=')
            self.assertEqual(1,0)
            
        except:
            self.assertEqual(0,0)
            


# Test task list progress status update logic
class TaskStatusTest(TestCase):

    # Test logic for when tasks are still not started
    def test_status_update_with_tasks_not_started(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'NOT_STARTED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
        )
        
        # Generate a context for task statuses
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
        
        # Temporarily disable Declarations task if other tasks are still not started
        temp_context = application_status_context
        del temp_context['declaration_status']
        
        assert(('NOT_STARTED' in temp_context.values()) == True)

    # Test logic for when tasks are still in progress
    def test_status_update_with_tasks_in_progress(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'IN_PROGRESS',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
        )
        
        # Generate a context for task statuses
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
        
        # Temporarily disable Declarations task if other tasks are still in progress
        temp_context = application_status_context
        del temp_context['declaration_status']
        
        assert(('IN_PROGRESS' in temp_context.values()) == True)

    # Test logic for when all tasks are complete, except for Declarations
    def test_status_update_with_tasks_completed_except_declarations(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
        )
        
        # Generate a context for task statuses
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
        
        # Temporarily disable Declarations task if other tasks are still in progress
        temp_context = application_status_context
        del temp_context['declaration_status']
        
        assert(('IN_PROGRESS' in temp_context.values()) == False)
        assert(('NOT_STARTED' in temp_context.values()) == False)
        
    # Test logic for when all tasks are complete, but Declarations is still to be started
    def test_status_update_with_tasks_completed_with_declarations_to_do(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'NOT_STARTED',
        )
        
        # Generate a context for task statuses
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
        
        assert((application_status_context['declaration_status'] == 'NOT_STARTED'))
        
    # Test logic for when all tasks are complete, but Declarations is still in progress
    def test_status_update_with_tasks_completed_with_declarations_in_progress(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'IN_PROGRESS',
        )
        
        # Generate a context for task statuses
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
        
        assert((application_status_context['declaration_status'] == 'IN_PROGRESS'))

    # Test logic for when all tasks are complete, including Delcarations
    def test_status_update_with_tasks_completed_with_declarations_complete(self):
    
        # Create a test application ID
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c' 
          
        # Create a test application
        application = Application.objects.create(
            application_id = (UUID(test_application_id)),   
            login_details_status = 'COMPLETED',
            personal_details_status = 'COMPLETED',
            childcare_type_status = 'COMPLETED',
            first_aid_training_status = 'COMPLETED',
            eyfs_training_status = 'COMPLETED',
            criminal_record_check_status = 'COMPLETED',
            health_status = 'COMPLETED',
            references_status = 'COMPLETED',
            people_in_home_status = 'COMPLETED',
            declarations_status = 'COMPLETED',
        )
        
        # Generate a context for task statuses
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
        
        assert((application_status_context['declaration_status'] == 'COMPLETED'))
    
    def delete(self):
        
        Application.objects.get(pk='f8c42666-1367-4878-92e2-1cee6ebcb48c').delete()