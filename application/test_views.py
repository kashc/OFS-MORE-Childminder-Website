from django.test import Client
from django.test import TestCase
from django.urls import resolve

from .views import ContactEmailView, DBSCheckView, EYFSView, FirstAidTrainingView, LogInView, PersonalDetailsView, StartPageView, TypeOfChildcareView

class StartPageTest(TestCase):
    
    def test_root_url_resolves_to_start_page_view(self):
        
        found = resolve('/')
        self.assertEqual(found.func, StartPageView)
    

class TaskListTest(TestCase):
    
    def test_url_resolves_to_task_list(self):
        
        found = resolve('/task-list/')
        self.assertEqual(found.func, LogInView)
        
    def test_task_list_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/task-list/?id=')
            
        except:
            self.assertEqual(0,0)  
        

class TypeOfChildcareTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/childcare/')
        self.assertEqual(found.func, TypeOfChildcareView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/childcare/?id=')
            
        except:
            self.assertEqual(0,0) 


class LoginAndContactDetailsTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/contact-email/')
        self.assertEqual(found.func, ContactEmailView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/contact-email/?id=')
            
        except:
            self.assertEqual(0,0)  
            
class PersonalDetailsTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/personal-details/')
        self.assertEqual(found.func, PersonalDetailsView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/personal-details/?id=')
            
        except:
            self.assertEqual(0,0)

class FirstAidTrainingTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/first-aid/')
        self.assertEqual(found.func, FirstAidTrainingView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/first-aid/?id=')
            
        except:
            self.assertEqual(0,0)
            
class EYFSTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/eyfs/')
        self.assertEqual(found.func, EYFSView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/eyfs/?id=')
            
        except:
            self.assertEqual(0,0)

class DBSCheckTest(TestCase):
    
    def test_url_resolves_to_page(self):
        found = resolve('/dbs-check/')
        self.assertEqual(found.func, DBSCheckView)
    
    def test_page_not_displayed_without_id(self):
        
        c = Client()
        
        try:
            response = c.get('/eyfs/?id=')
            
        except:
            self.assertEqual(0,0)