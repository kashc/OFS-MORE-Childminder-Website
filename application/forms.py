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

from .models import Applicant_Names, Applicant_Personal_Details, Childcare_Type, Criminal_Record_Check, First_Aid_Training, Login_And_Contact_Details, Health_Declaration_Booklet, References

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
        required = False,
        widget = InlineCheckboxSelectMultiple,
        choices = CHILDCARE_AGE_CHOICES,
        label = '',
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
        if Login_And_Contact_Details.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['email_address'].initial = Login_And_Contact_Details.objects.get(application_id=self.application_id_local).email
    
    def clean_email_address(self):
        
        email_address = self.cleaned_data['email_address']
            
        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            
            raise forms.ValidationError('Please enter a valid e-mail address.')
        
        return email_address

# Your login and contact details form: phone numbers   
class ContactPhone(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    mobile_number = forms.CharField(label = 'Mobile phone number')
    add_phone_number = forms.CharField(label = 'Additional phone number (optional)', required = False)
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(ContactPhone, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form
        if Login_And_Contact_Details.objects.filter(application_id=self.application_id_local).count() > 0:
            
            self.fields['mobile_number'].initial = Login_And_Contact_Details.objects.get(application_id=self.application_id_local).mobile_number
            self.fields['add_phone_number'].initial = Login_And_Contact_Details.objects.get(application_id=self.application_id_local).add_phone_number

    def clean_mobile_number(self):
        
        mobile_number = self.cleaned_data['mobile_number']
        
        if re.match("^(07\d{8,12}|447\d{7,11})$", mobile_number) is None:
            
            raise forms.ValidationError('Please enter a valid mobile number.')
        
        return mobile_number

    def clean_add_phone_number(self):
        
        add_phone_number = self.cleaned_data['add_phone_number']
            
        if re.match("^(0\d{8,12}|447\d{7,11})$", add_phone_number) is None:
            
            raise forms.ValidationError('Please enter a valid phone number.')
        
        return add_phone_number
    

# Your login and contact details form: summary page  
class ContactSummary(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    

# Your login and contact details form: knowledge-based question 
class Question(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    question = forms.CharField(label = 'Knowledge based question', required = False)

    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(Question, self).__init__(*args, **kwargs)


# Your personal details form    
class PersonalDetails(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    
    options = (('yes', 'Yes'), ('no', 'No'))

    first_name = forms.CharField(label = 'First name')
    middle_names = forms.CharField(label = 'Middle names (optional)', required = False)
    last_name = forms.CharField(label = 'Last name')
    name_change = forms.ChoiceField(label = 'Have you ever changed your name?', choices = options, widget = InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetails, self).__init__(*args, **kwargs)
        
        # If information was previously entered, display it on the form        
        if Applicant_Personal_Details.objects.filter(application_id=self.application_id_local).count() > 0:
            
            personal_detail_id = Applicant_Personal_Details.objects.get(application_id = self.application_id_local).personal_detail_id
            
            self.fields['first_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).first_name
            self.fields['middle_names'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).middle_names
            self.fields['last_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).last_name
            self.fields['name_change'].initial = 'yes'


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
            self.fields['course_date'].initial = [First_Aid_Training.objects.get(application_id=self.application_id_local).course_day,First_Aid_Training.objects.get(application_id=self.application_id_local).course_month,First_Aid_Training.objects.get(application_id=self.application_id_local).course_year]
 

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


# Application saved form
class ApplicationSaved(GOVUKForm):
    
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True