'''
Created on 07 Dec 2017

OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Forms --

@author: Informed Solutions
'''

from django import forms
from govuk_forms.fields import SplitDateField
from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineCheckboxSelectMultiple, InlineRadioSelect, RadioSelect

from application.models import Application, Applicant_Names, Applicant_Personal_Details, Childcare_Type, Criminal_Record_Check, First_Aid_Training, Login_And_Contact_Details, Health_Declaration_Booklet, References, \
    Applicant_Home_Address

import re 


# Type of childcare form
class TypeOfChildcare(forms.Form):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    CHILDCARE_AGE_CHOICES = (
        ('0-5', 'Birth up to 5 years old'),
        ('5-8', '5 to 8 years old'),
        ('8over', '8 years and over'),
    )
    
    type_of_childcare = forms.MultipleChoiceField(
        required=False,
        widget=InlineCheckboxSelectMultiple,
        choices=CHILDCARE_AGE_CHOICES,
        label='',
    )
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(TypeOfChildcare, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        if Childcare_Type.objects.filter(application_id=self.application_id_local).count() > 0:
            
            zero_to_five_status = Childcare_Type.objects.get(application_id=self.application_id_local).zero_to_five
            five_to_eight_status = Childcare_Type.objects.get(application_id=self.application_id_local).five_to_eight
            eight_plus_status = Childcare_Type.objects.get(application_id=self.application_id_local).eight_plus
            
            if (zero_to_five_status == True) & (five_to_eight_status == True) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8', '8over']
            
            elif (zero_to_five_status == True) & (five_to_eight_status == True) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8']
            
            elif (zero_to_five_status == True) & (five_to_eight_status == False) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['0-5', '8over']

            elif (zero_to_five_status == False) & (five_to_eight_status == True) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['5-8', '8over']

            elif (zero_to_five_status == True) & (five_to_eight_status == False) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['0-5']

            elif (zero_to_five_status == False) & (five_to_eight_status == True) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['5-8']
                
            elif (zero_to_five_status == False) & (five_to_eight_status == False) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['8over']

            elif (zero_to_five_status == False) & (five_to_eight_status == False) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = []


class EmailLogin(forms.ModelForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    class Meta:
        model = Login_And_Contact_Details
        fields = ('email',)
        email_address = forms.EmailField()


# Your login and contact details form: e-mail address   
class ContactEmail(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    email_address = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(ContactEmail, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        if Application.objects.filter(application_id=self.application_id_local).count() > 0:
            
            this_user = Application.objects.get(pk=self.application_id_local)
            login_id = this_user.login_id.login_id
            
            if Login_And_Contact_Details.objects.get(login_id=login_id).login_id != '':
            
                self.fields['email_address'].initial = Login_And_Contact_Details.objects.get(login_id=login_id).email
    
    # Email address validation
    def clean_email_address(self):
        
        email_address = self.cleaned_data['email_address']
            
        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            
            raise forms.ValidationError('Please enter a valid e-mail address.')
        
        return email_address


# Your login and contact details form: phone numbers   
class ContactPhone(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    mobile_number = forms.CharField(label='Mobile phone number')
    add_phone_number = forms.CharField(label='Additional phone number (optional)', required=False)
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(ContactPhone, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        if Application.objects.filter(application_id=self.application_id_local).count() > 0:
            
            this_user = Application.objects.get(pk=self.application_id_local)
            login_id = this_user.login_id.login_id
            
            self.fields['mobile_number'].initial = Login_And_Contact_Details.objects.get(login_id=login_id).mobile_number
            self.fields['add_phone_number'].initial = Login_And_Contact_Details.objects.get(login_id=login_id).add_phone_number

    # Mobile number validation
    def clean_mobile_number(self):
        
        mobile_number = self.cleaned_data['mobile_number']
        
        if re.match("^(07\d{8,12}|447\d{7,11})$", mobile_number) is None:
            
            raise forms.ValidationError('Please enter a valid mobile number.')
            
        if len(mobile_number) > 11:
            
            raise forms.ValidationError('Please enter a valid mobile number.')
        
        return mobile_number

    # Phone number validation
    def clean_add_phone_number(self):
        
        add_phone_number = self.cleaned_data['add_phone_number']
            
        if add_phone_number != '':
        
            if re.match("^(0\d{8,12}|447\d{7,11})$", add_phone_number) is None:
                
                raise forms.ValidationError('Please enter a valid phone number.')
                
            if len(add_phone_number) > 11:
            
                raise forms.ValidationError('Please enter a valid phone number.')
        
        return add_phone_number
    

# Your login and contact details form: knowledge-based question 
class Question(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    question = forms.CharField(label='Knowledge based question', required=False)

    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(Question, self).__init__(*args, **kwargs)
        

# Your login and contact details form: summary page  
class ContactSummary(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    

# Your personal details form: guidance page  
class PersonalDetailsGuidance(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your personal details form: names   
class PersonalDetailsName(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    first_name = forms.CharField(label='First name')
    middle_names = forms.CharField(label='Middle names (if you have any)', required=False)
    last_name = forms.CharField(label='Last name')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsName, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form        
        if Applicant_Personal_Details.objects.filter(application_id=self.application_id_local).count() > 0:
            
            personal_detail_id = Applicant_Personal_Details.objects.get(application_id=self.application_id_local).personal_detail_id
            
            self.fields['first_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).first_name
            self.fields['middle_names'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).middle_names
            self.fields['last_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).last_name
    
    # First name validation
    def clean_first_name(self):
        
        first_name = self.cleaned_data['first_name']
            
        if re.match("^[A-Za-z-]+$", first_name) is None:
                
            raise forms.ValidationError('Please enter a valid name.')
        
        return first_name
    
    # Middle names validation
    def clean_middle_names(self):
        
        middle_names = self.cleaned_data['middle_names']
            
        if re.match("^[A-Za-z-]+$", middle_names) is None:
                
            raise forms.ValidationError('Please enter a valid name.')
        
        return middle_names
    
    # Last name validation
    def clean_last_name(self):
        
        last_name = self.cleaned_data['last_name']
            
        if re.match("^[A-Za-z-]+$", last_name) is None:
                
            raise forms.ValidationError('Please enter a valid name.')
        
        return last_name


# Your personal details form: date of birth 
class PersonalDetailsDOB(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    date_of_birth = SplitDateField(label='Date of birth', help_text='For example, 31 03 1980')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsDOB, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form        
        if Applicant_Personal_Details.objects.filter(application_id=self.application_id_local).count() > 0:
            
            self.fields['date_of_birth'].initial = [Applicant_Personal_Details.objects.get(application_id=self.application_id_local).birth_day, Applicant_Personal_Details.objects.get(application_id=self.application_id_local).birth_month, Applicant_Personal_Details.objects.get(application_id=self.application_id_local).birth_year]

    # First name validation
    def clean_date_of_birth(self):
        
        birth_day = self.cleaned_data['date_of_birth'].day
        birth_month = self.cleaned_data['date_of_birth'].month
        birth_year = self.cleaned_data['date_of_birth'].year
            
        if re.match("^(0[1-9]|[12]\d|3[01])$", str(birth_day)) is None:
                
            raise forms.ValidationError('Please enter a valid date.')
        
        elif re.match("^(0?[1-9]|1[012])$", str(birth_month)) is None:
                
            raise forms.ValidationError('Please enter a valid date.')

        elif re.match("^\d{4}$", str(birth_year)) is None:
                
            raise forms.ValidationError('Please enter a valid date.')
        
        return birth_day, birth_month, birth_year
    

# Your personal details form: home address   
class PersonalDetailsHomeAddress(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsHomeAddress, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        personal_detail_id = Applicant_Personal_Details.objects.get(application_id=self.application_id_local).personal_detail_id
            
        if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id).count() > 0:
            
            personal_detail_id = Applicant_Personal_Details.objects.get(application_id=self.application_id_local).personal_detail_id
            
            self.fields['postcode'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).postcode
            

# Your personal details form: home address   
class PersonalDetailsHomeAddressManual(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    street_name_and_number = forms.CharField(label='Street name and number')
    street_name_and_number2 = forms.CharField(label='Street name and number 2', required=False)
    town = forms.CharField(label='Town or city')
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsHomeAddressManual, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        personal_detail_id = Applicant_Personal_Details.objects.get(application_id=self.application_id_local).personal_detail_id
            
        if Applicant_Home_Address.objects.filter(personal_detail_id=personal_detail_id).count() > 0:
            
            personal_detail_id = Applicant_Personal_Details.objects.get(application_id=self.application_id_local).personal_detail_id
            
            self.fields['street_name_and_number'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).street_line1
            self.fields['street_name_and_number2'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).street_line2
            self.fields['town'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).town
            self.fields['county'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).county
            self.fields['postcode'].initial = Applicant_Home_Address.objects.get(personal_detail_id=personal_detail_id).postcode
    
    # Town validation
    def clean_town(self):
        
        town = self.cleaned_data['town']
            
        if re.match("^[A-Za-z-]+$", town) is None:
                
            raise forms.ValidationError('Please enter a valid town.')
        
        return town   
    
    # County validation
    def clean_county(self):
        
        county = self.cleaned_data['county']
            
        if county != '':
        
            if re.match("^[A-Za-z-]+$", county) is None:
                
                raise forms.ValidationError('Please enter a valid county.')
        
        return county
    
    # Postcode validation
    def clean_postcode(self):
        
        postcode = self.cleaned_data['postcode']
            
        if re.match("^[A-Za-z0-9 ]+$", postcode) is None:
                
            raise forms.ValidationError('Please enter a valid postcode.')
        
        return postcode


# First aid training form
class FirstAidTraining(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    first_aid_training_organisation = forms.CharField(label='First aid training organisation')
    title_of_training_course = forms.CharField(label='Title of training course')
    course_date = SplitDateField(label='Course date', help_text='For example, 31 03 1980')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(FirstAidTraining, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if First_Aid_Training.objects.filter(application_id=self.application_id_local).count() > 0:
            
            self.fields['first_aid_training_organisation'].initial = First_Aid_Training.objects.get(application_id=self.application_id_local).training_organisation
            self.fields['title_of_training_course'].initial = First_Aid_Training.objects.get(application_id=self.application_id_local).course_title
            self.fields['course_date'].initial = [First_Aid_Training.objects.get(application_id=self.application_id_local).course_day, First_Aid_Training.objects.get(application_id=self.application_id_local).course_month, First_Aid_Training.objects.get(application_id=self.application_id_local).course_year]
 

# Early Years knowledge form
class EYFS(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

 
# Your criminal record (DBS) check form   
class DBSCheck(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    options = (('True', 'Yes'), ('False', 'No'))

    dbs_certificate_number = forms.IntegerField(label='DBS certificate number', help_text='12-digit number on your certificate')
    convictions = forms.ChoiceField(label='Do you have any cautions or convictions?', help_text='Include any information recorded on your certificate', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(DBSCheck, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form 
        if Criminal_Record_Check.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['dbs_certificate_number'].initial = Criminal_Record_Check.objects.get(application_id=self.application_id_local).dbs_certificate_number
            self.fields['convictions'].initial = Criminal_Record_Check.objects.get(application_id=self.application_id_local).cautions_convictions


# Your health form
class HealthDeclarationBooklet(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    options = (('True', 'Yes'), ('False', 'No'))
    
    walking_bending = forms.ChoiceField(label='Walking, bending, kneeling or lifting a child', choices=options, widget=InlineRadioSelect)
    asthma_breathing = forms.ChoiceField(label='Asthma or breathing difficulties', choices=options, widget=InlineRadioSelect)
    heart_disease = forms.ChoiceField(label='Heart disease', choices=options, widget=InlineRadioSelect)
    blackout_epilepsy = forms.ChoiceField(label='Blackouts, fits, epilepsy or fainting', choices=options, widget=InlineRadioSelect)
    mental_health = forms.ChoiceField(label='Depression, anxiety, panic attacks or mood swings', choices=options, widget=InlineRadioSelect)
    alcohol_drugs = forms.ChoiceField(label='Alcohol or drugs', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(HealthDeclarationBooklet, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form 
        if Health_Declaration_Booklet.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['walking_bending'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).movement_problems
            self.fields['asthma_breathing'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).breathing_problems
            self.fields['heart_disease'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).heart_disease
            self.fields['blackout_epilepsy'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).blackout_epilepsy
            self.fields['mental_health'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).mental_health_problems
            self.fields['alcohol_drugs'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).alcohol_drug_problems 


# 2 references form
class ReferenceForm(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    relationship = forms.CharField(label='How do they know you?')
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(ReferenceForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if References.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['first_name'].initial = References.objects.get(application_id=self.application_id_local).first_name
            self.fields['last_name'].initial = References.objects.get(application_id=self.application_id_local).last_name
            self.fields['relationship'].initial = References.objects.get(application_id=self.application_id_local).relationship  


# People in your home form     
class OtherPeople(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True 


# Declaration form
class Declaration(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Confirm your details form
class Confirm(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Payment form
class Payment(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    options = (('Credit', 'Credit or debit card'), ('PayPal', 'PayPal'))
    
    payment_method = forms.ChoiceField(label='How would you like to pay?', choices=options, widget=RadioSelect)


class PaymentDetails(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    card_type_options = (('visa', 'Visa'), ('mastercard', 'Mastercard'), ('american_express', 'American Express'), ('maestro', 'Maestro'))
    
    card_type = forms.ChoiceField(label='Card type', choices=card_type_options)
    card_number = forms.IntegerField(label='Card number')
    expiry_date = SplitDateField(label='Expiry date')
    cardholders_name = forms.CharField(label="Cardholders name")
    card_security_code = forms.IntegerField(label='Card security code')


# Application saved form
class ApplicationSaved(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
