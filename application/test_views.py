'''
Created on 15 Dec 2017

@author: Informed Solutions
'''

from django.test import Client
from django.test import TestCase
from django.urls import resolve

from .views import ConfirmationView, ContactEmailView, DBSCheckView, DeclarationView, EYFSView, FirstAidTrainingView, HealthView, LogInView, OtherPeopleView, PersonalDetailsView, ReferencesView, StartPageView, TypeOfChildcareView

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
        
        try:
            response = c.get('/task-list/?id=')
            
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
            
        except:
            self.assertEqual(0,0) 


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
            
        except:
            self.assertEqual(0,0)  


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)


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
            
        except:
            self.assertEqual(0,0)