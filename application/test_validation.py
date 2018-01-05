'''
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Validation Unit Tests --

@author: Informed Solutions
'''


from django.test import TestCase

import re

from datetime import date



# Test validation for Your login details
class Test_Login_And_Contact_Details_Validation(TestCase):
    
    # Test validation for correct email
    def test_correct_email(self):
        
        test_email = 'erik.odense@gmail.com'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) != None)

    # Test validation for correct email
    def test_correct_email2(self):
        
        test_email = 'erikodense123@gmail.com'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) != None)

    # Test validation for correct email
    def test_correct_email3(self):
        
        test_email = 'erik.tolstrup.odense@gmail.com'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) != None)       

    # Test validation for incorrect email
    def test_incorrect_email(self):
        
        test_email = 'erik.odense'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) == None)

    # Test validation for incorrect email
    def test_incorrect_email2(self):
        
        test_email = 'erik.odense@'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) == None)  

    # Test validation for incorrect email
    def test_incorrect_email3(self):
        
        test_email = 'erik.odense@gmail'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) == None)

    # Test validation for incorrect email
    def test_incorrect_email4(self):
        
        test_email = 'erik.odense@gmail.'
        
        assert(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", test_email) == None)
    
    # Test validation for correct mobile number
    def test_correct_mobile_number(self):
        
        test_mobile_number = '07783446526'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) != None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number(self):
        
        test_mobile_number = '7783446526'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number2(self):
        
        test_mobile_number = '08783446526'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number3(self):
        
        test_mobile_number = '0778344652645677754'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number4(self):
        
        test_mobile_number = 'dfasdggregas'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number5(self):
        
        test_mobile_number = 'dsfdsf13'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number6(self):
        
        test_mobile_number = '0778abcdrewr'
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for incorrect mobile number
    def test_incorrect_mobile_number7(self):
        
        test_mobile_number = "07783'4352"
    
        assert(re.match("^(07\d{8,12}|447\d{7,11})$", test_mobile_number) == None)

    # Test validation for correct mobile number
    def test_correct_mobile_number_length(self):
        
        test_mobile_number = '0778344652645677754'
    
        assert(len(test_mobile_number) > 11) 

    # Test validation for incorrect mobile number (too long)
    def test_incorrect_mobile_number_too_long(self):
        
        test_mobile_number = '07783446526'
    
        assert(len(test_mobile_number) <= 11)
    
    # Test validation for correct phone number
    def test_correct_phone_number(self):
        
        test_phone_number = '0161445627'
        
        assert(re.match("^(0\d{8,12}|447\d{7,11})$", test_phone_number) != None)

    # Test validation for incorrect phone number
    def test_incorrect_phone_number(self):
        
        test_phone_number = '161445627'
        
        assert(re.match("^(0\d{8,12}|447\d{7,11})$", test_phone_number) == None)     
             

# Test validation for Your personal details
class Test_Personal_Details_Validation(TestCase):
    
    # Test validation for correct name
    def test_correct_name(self):
        
        # Create a correct name
        test_name = 'Erik'
        
        # Verify that the name matches the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) != None)

    # Test validation for correct name
    def test_correct_name2(self):
        
        # Create a correct name
        test_name = 'Anne-Marie'
        
        # Verify that the name matches the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) != None)

    # Test validation for correct name
    def test_correct_name3(self):
        
        # Create a correct name
        test_name = 'erik'
        
        # Verify that the name matches the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) != None)

    # Test validation for correct name
    def test_correct_name4(self):
        
        # Create a correct name
        test_name = 'anne-marie'
        
        # Verify that the name matches the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) != None)

    # Test validation for correct name
    def test_correct_name5(self):
        
        # Create a correct name
        test_name = 'Eun Ji'
        
        # Verify that the name matches the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) != None)

    # Test validation for incorrect name
    def test_incorrect_name(self):
        
        # Create an incorrect name
        test_name = '1234'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name2(self):
        
        # Create an incorrect name
        test_name = '1234a'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name3(self):
        
        # Create an incorrect name
        test_name = '1234A'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name4(self):
        
        # Create an incorrect name
        test_name = '1234-'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name5(self):
        
        # Create an incorrect name
        test_name = '1234-a'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name6(self):
        
        # Create an incorrect name
        test_name = '1234-A'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)

    # Test validation for incorrect name
    def test_incorrect_name7(self):
        
        # Create an incorrect name
        test_name = '1234-Aa'
        
        # Verify that the name does not match the RegEx
        assert(re.match("^[A-Za-z- ]+$", test_name) == None)
    
    # Test validation for legal age to childmind
    def test_legal_age_to_childmind(self):
        
        test_applicant_dob = date(1995, 4, 20)
        test_date = date(2018, 1, 5)
        age = test_date.year - test_applicant_dob.year - ((test_date.month, test_date.day) < (test_applicant_dob.month, test_applicant_dob.day))
        
        assert(age > 18)

    # Test validation for illegal age to childmind
    def test_illegal_age_to_childmind(self):
        
        test_applicant_dob = date(2014, 2, 1)
        test_date = date(2018, 1, 5)
        age = test_date.year - test_applicant_dob.year - ((test_date.month, test_date.day) < (test_applicant_dob.month, test_applicant_dob.day))
        
        assert(age < 18)
    
    # Test address string that is too long
    def test_address_string_that_is_too_long(self):
        
        test_string = 'LlanfairpwllgwyngyllgogerychwyrndrbwllllantisiliogogogochLlanfairpwllgwyngyllgogerychwyrndrbwllllantisiliogogogoch'
        
        assert(len(test_string) > 100)

    # Test address string that is not too long
    def test_address_string_that_is_not_too_long(self):
        
        test_string = 'Llanfairpwllgwyngyllgogerychwyrndrbwllllantisiliogogogoch'
        
        assert(len(test_string) <= 100)
    
    # Test valid postcode
    def test_valid_postcode(self):
        
        test_postcode = 'WA14 4PA'
        
        assert(re.match("^[A-Za-z0-9 ]{1,8}$", test_postcode) != None)

    # Test valid postcode without space
    def test_valid_postcode_without_space(self):
        
        test_postcode = 'WA144PA'
        
        assert(re.match("^[A-Za-z0-9 ]{1,8}$", test_postcode) != None)

    # Test invalid postcode
    def test_invalid_postcode(self):
        
        test_postcode = '!%WA14'
        
        assert(re.match("^[A-Za-z0-9 ]{1,8}$", test_postcode) == None)

    # Test invalid postcode (too long)
    def test_invalid_postcode_too_long(self):
        
        test_postcode = 'WA14 4PAAAAAA'
        
        assert(re.match("^[A-Za-z0-9 ]{1,8}$", test_postcode) == None)

    # Test invalid postcode (too long)
    def test_invalid_postcode_too_long2(self):
        
        test_postcode = 'WA144PAAAAAA'
        
        assert(re.match("^[A-Za-z0-9 ]{1,8}$", test_postcode) == None)